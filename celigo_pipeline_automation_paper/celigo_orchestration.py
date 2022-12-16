import logging
import multiprocessing
import os
import pathlib
import sys
import time
import typing

from .celigo_single_image import CeligoSingleImage

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


def run_all(
    raw_image_path: str,
    working_dir: str = "",
):
    """
    Process Celigo Image from `raw_image_path`. Submits jobs for Image Downsampling,
    Image Ilastik Processing, and Image Celigo Processing. After job completion,
    Image Metrics are uploaded to an external database.

    Parameters
    ----------
    raw_image_path : str
        Path must point to a .Tiff image produced by the Celigo camera.
    working_dir: str
        (Optional) Path to directory to store outputs, directory must be accessible by HPC.

    """
    # Construct Image
    image = CeligoSingleImage(raw_image_path, working_dir)

    downsample_output_file_path = image.downsample()
    job_complete_check([downsample_output_file_path])

    ilastik_output_file_path = image.run_ilastik()
    job_complete_check([ilastik_output_file_path])

    cellprofiler_output_file_paths = image.run_cellprofiler()
    job_complete_check(cellprofiler_output_file_paths)

    log.info("Process Complete.")


def job_complete_check(
    filelist: typing.List[pathlib.Path],
):
    # Main Logic Loop: waiting for files to exist or maximum wait-time reached.
    while not all([os.path.isfile(f) for f in filelist]):
        time.sleep(5)
    return


def run_all_dir(
    dir_path: str,
    chunk_size: int = 30,
    working_dir: str = "",
):
    """
    Process Celigo Images from a directory (`dir_path`) and all sub directories in batches.
    Submits jobs for Images Downsampling, Images Ilastik Processing, and Images Celigo Processing.
    After job completion, Images Metrics are uploaded to an external database.

    Parameters
    ----------
    dir_path : str
        Path must point to a Directory. Path must be accessable
        from SLURM (ISILON[OK])
    chunk_size: int
        (Optional) Size of each Batch to run simultaniously. Default is set to 30.
        For 6 well it is reccomended that you overwrite this number (3-5).
    working_dir: str
        (Optional) Path to directory to store outputs, directory must be accessable by HPC.
    """

    # loop through all files
    for _, _, files in os.walk(dir_path):
        run_list(
            filelist=files,
            chunk_size=chunk_size,
            working_dir=working_dir,
        )


def run_list(
    filelist: typing.List[str],
    working_dir: str,
    chunk_size: int,
):
    """Process Celigo Images from a list of files  (`filelist`) and all sub directories in batches.
    Submits jobs for Images Downsampling, Images Ilastik Processing, and Images Celigo Processing.
    After job completion, Images Metrics are uploaded to an external database.

    Parameters
    ----------
    filelist : list[str]
        list of paths, paths must point to a Directory. Path must be accessable
        from SLURM (ISILON[OK])
    chunk_size: int
        (Optional) Size of each Batch to run simultaniously. Default is set to 30.
        For 6 well it is reccomended that you overwrite this number (3-5).
    working_dir: str
        (Optional) path to directory to store outputs, directory must be accessable by HPC.
    """
    processes = []
    start = time.perf_counter()
    for files in list(split_list_to_chunks(filelist, chunk_size)):
        for file in files:
            # Celigo files are denoted with the barcode header of 350000
            p = multiprocessing.Process(
                target=run_all,
                args=[
                    file,
                    working_dir,
                ],
            )
            p.start()
            processes.append(p)
        for process in processes:
            process.join()

    finish = time.perf_counter()

    log.info(f"Finished in {round(finish-start,2)} second(s)")


# Funciton for generating chunks from a list
def split_list_to_chunks(
    list_a: typing.List,
    chunk_size: int,
):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i : i + chunk_size]
