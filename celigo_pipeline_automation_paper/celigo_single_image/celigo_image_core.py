import importlib.resources as pkg_resources
import json
import logging
import os
from pathlib import Path
import pwd
import shutil
import subprocess

from jinja2 import Environment, PackageLoader

from .. import pipelines
from .celigo_image import CeligoImage

log = logging.getLogger(__name__)

with open(Path(__file__).parent / "../bin/resource_paths.json", "r") as f:
    USER_CELIGO_PATHS = json.load(f)

SIX_WELL_PIPELINES = {
    "rescale_pipeline": "6_well_rescale_pipeline.cppipe",
    "cellprofiler_pipeline": "6_well_cellprofiler_pipeline.cppipe",
    "ilp": USER_CELIGO_PATHS["6_well_ilp"],
}

NINETYSIX_WELL_PIPELINES = {
    "rescale_pipeline": "96_well_rescale_pipeline.cppipe",
    "classification_model": "colonymorphology.model",
    "cellprofiler_pipeline_template": "96_well_pipeline_tempalate.j2",
    "ilp": USER_CELIGO_PATHS["96_well_ilp"],
}


class CeligoSingleImage(CeligoImage):
    """This Class provides utility functions for the Celigo
    pipeline to prepare single celigo images.

    """

    def __init__(
        self,
        raw_image_path: str,
        working_dir: str = "",
    ) -> None:
        """Constructor.

        Parameters
        ----------
        raw_image_path : str
            Raw celigo image path. This path is used to copy a version of the image to SLURM for
            processing.
        working_directory:
            (Optional) Path to directory to store outputs, directory must be accessible by HPC.
            Default is set to: /home/USERID/FILENAME
        """
        if not os.path.exists(raw_image_path):
            raise FileNotFoundError(f"{raw_image_path} does not exist!")
        raw_image = Path(raw_image_path)
        log.info(f"Executing Celigo pipeline on {raw_image.name}.")

        if os.path.getsize(raw_image_path) > 100000000:
            self.image_type = "6 Well"
            self.pipeline_table = SIX_WELL_PIPELINES
        else:
            self.image_type = "96 Well"
            self.pipeline_table = NINETYSIX_WELL_PIPELINES

        log.info(f"File: {raw_image.name} has been designated type {self.image_type}.")

        # Directory Name, used to create working directory.
        self.tempdirname = Path(raw_image_path).with_suffix("").name

        # Working Directory Creation
        if working_dir == "":
            if not os.path.exists(
                f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
            ):
                os.mkdir(f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}")
            self.working_dir = Path(
                f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
            )
        else:
            if not os.path.exists(f"{working_dir}/{self.tempdirname}"):
                os.mkdir(f"{working_dir}/{self.tempdirname}")
            self.working_dir = Path(f"{working_dir}/{self.tempdirname}")

        # Copying Image to working directory.
        self.raw_image_path = Path(raw_image_path)
        shutil.copyfile(
            self.raw_image_path, f"{self.working_dir}/{self.raw_image_path.name}"
        )
        self.image_path = Path(f"{self.working_dir}/{self.raw_image_path.name}")

        # Creating pipeline paths for templates
        with pkg_resources.path(
            pipelines, self.pipeline_table["rescale_pipeline"]
        ) as p:
            self.rescale_pipeline_path = p

        # Establish Cellprofiler pipeline for 96 Well
        if self.image_type == "96 Well":

            # Import classification model
            with pkg_resources.path(
                pipelines, self.pipeline_table["classification_model"]
            ) as p:
                self.classification_model_path = p

            # Creating template for 96 well processing
            script_config = {
                "classifier_path": str(self.classification_model_path.parent),
            }
            jinja_env = Environment(
                loader=PackageLoader(
                    package_name="celigo_pipeline_automation_paper",
                    package_path="templates",
                )
            )
            script_body = jinja_env.get_template(
                self.pipeline_table["cellprofiler_pipeline_template"]
            ).render(script_config)

            with open(self.working_dir / "cellprofiler_pipeline.cppipe", "w+") as rsh:
                rsh.write(script_body)
            self.cellprofiler_pipeline_path = (
                self.working_dir / "cellprofiler_pipeline.cppipe"
            )

        # Establish Cellprofiler pipeline for 6 Well
        else:
            with pkg_resources.path(
                pipelines,
                self.pipeline_table["cellprofiler_pipeline"],
            ) as p:
                self.cellprofiler_pipeline_path = p

    def downsample(self):
        """downsample raw images for higher processing speed and streamlining of
        later steps

        Returns
        -------
        pathlib.Path
            Path to resized image.
        """

        # Generates filelist for resize pipeline
        with open(self.working_dir / "resize_filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")
        self.resize_filelist_path = self.working_dir / "resize_filelist.txt"

        # Defines variables for bash script
        script_config = {
            "filelist_path": str(self.resize_filelist_path),
            "output_path": str(self.working_dir),
            "pipeline_path": str(self.rescale_pipeline_path),
            "resize_conda": USER_CELIGO_PATHS["cellprofiler_conda"],
            "activate_cellprofiler": USER_CELIGO_PATHS[
                "cellprofiler_conda_environment"
            ],
        }

        # Generates script_body from existing templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_automation_paper",
                package_path="templates",
            )
        )
        script_body = jinja_env.get_template("resize_template.j2").render(script_config)

        # Creates bash script locally.
        with open(self.working_dir / "resize.sh", "w+") as rsh:
            rsh.write(script_body)

        # Runs resize on slurm
        self.output = subprocess.call(["sh", f"{str(self.working_dir)}/resize.sh"])

        # Sets path to resized image to image path for future use
        self.image_path = (
            self.image_path.parent
            / f"{self.image_path.with_suffix('').name}_rescale.tiff"
        )
        return self.image_path

    def run_ilastik(self):
        """Applies the Ilastik Pipeline processing to the downsampled image to
        produce a Probability map of the prior image.

        Returns
        -------
        pathlib.Path
            Path to Ilastik Probablility Map.
        """

        # Parameters to input to bash script template
        script_config = {
            "image_path": f"'{str( self.image_path)}'",
            "output_path": f"'{str(self.image_path.with_suffix(''))}_probabilities.tiff'",
            "ilastik_conda": USER_CELIGO_PATHS["ilastik_conda"],
            "ilastik_conda_environment": USER_CELIGO_PATHS["ilastik_conda_environment"],
            "run_ilastik": USER_CELIGO_PATHS["run_ilastik"],
            "ilp": self.pipeline_table["ilp"],
        }

        # Generates script for SLURM submission from templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_automation_paper",
                package_path="templates",
            )
        )
        script_body = jinja_env.get_template("ilastik_template.j2").render(
            script_config
        )
        with open(self.working_dir / "ilastik.sh", "w+") as rsh:
            rsh.write(script_body)

        # Submit bash script ilastik.sh on SLURM
        self.output = subprocess.call(
            [
                "sh",
                f"{str(self.working_dir)}/ilastik.sh",
            ]
        )

        # Creates filelist.txt
        with open(self.working_dir / "filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")
            rfl.write(str(self.image_path.with_suffix("")) + "_probabilities.tiff")

        self.filelist_path = self.working_dir / "filelist.txt"
        return Path(f"{self.image_path.with_suffix('')}_probabilities.tiff")

    def run_cellprofiler(self):
        """Applies the Cell Profiler Pipeline processing to the downsampled image using the Ilastik
        probabilities to produce a outlined cell profile and a series of metrics.

        Returns
        -------
            List[pathlib.Path]
            A list of paths to desired output files, with the following layout:
                [0] : Outline Image
                [1] : ColonyDATA.csv
                [2] : ImageDATA.csv
                [3] : PoorMorphObjectDATA.csv
        """

        # Parameters to input to bash script template.
        script_config = {
            "filelist_path": str(self.filelist_path),
            "output_dir": str(self.working_dir / "cell_profiler_outputs"),
            "pipeline_path": str(self.cellprofiler_pipeline_path),
            "cellprofiler_conda": USER_CELIGO_PATHS["cellprofiler_conda"],
            "activate_cellprofiler": USER_CELIGO_PATHS[
                "cellprofiler_conda_environment"
            ],
        }

        # Generates script for SLURM submission from templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_automation_paper",
                package_path="templates",
            )
        )
        script_body = jinja_env.get_template("cellprofiler_template.j2").render(
            script_config
        )
        with open(self.working_dir / "cellprofiler.sh", "w+") as rsh:
            rsh.write(script_body)

        # Submit bash script cellprofiler.sh on SLURM
        self.output = subprocess.call(
            [
                "sh",
                f"{str(self.working_dir)}/cellprofiler.sh",
            ]
        )

        # Set output path
        self.cell_profiler_output_path = self.working_dir / "cell_profiler_outputs"
        return (
            [
                Path(
                    f"{script_config['output_dir']}/{self.image_path.with_suffix('').name}_outlines.png"
                ),
                Path(f"{script_config['output_dir']}/ColonyDATA.csv"),
                Path(f"{script_config['output_dir']}/ImageDATA.csv"),
                Path(f"{script_config['output_dir']}/PoorMorphObjectDATA.csv"),
            ],
        )
