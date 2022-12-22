# celigo_pipeline_automation_paper

[![Build Status](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/workflows/Build%20Main/badge.svg)](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/actions)
[![Documentation](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/workflows/Documentation/badge.svg)](https://BrianWhitneyAI.github.io/celigo_pipeline_automation_paper/)
[![Code Coverage](https://codecov.io/gh/BrianWhitneyAI/celigo_pipeline_automation_paper/branch/main/graph/badge.svg)](https://codecov.io/gh/BrianWhitneyAI/celigo_pipeline_automation_paper)

`celigo_pipeline_automation_paper` 

- [Overview](#overview)
- [Documentation](#documentation)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Demos](#demos)
- [Example Outputs](#example-outputs)
- [License](#license)

# Overview
``celigo_pipeline_automation_paper`` is a companion package for **Automated hiPSC culture and sample preparation for 3D live cell microscopy**. It contains algorithms to run an automated image-based colony segmentation and feature extraction pipeline to predict cell count and select wells with consistent morphology for high resolution 3D microscopy.

# Documentation

For full package documentation please visit [aics-int.github.io/celigo_pipeline_automation_paper](https://aics-int.github.io/celigo_pipeline_automation_paper/).

# System Requirements
## Hardware requirements
`celigo_pipeline_automation_paper` package requires only a standard computer with enough RAM to support the in-memory operations.

Memory Requirements:
* Six Well: 64 GB (~ 20 min runtime)
* Ninety Six Well: 16 GB (~ 1 min runtime)

*Note: This process was originally intended for use in a High Processing Cluster. Running single files is possible with the given memory requirements, however, running tandem processes on a local computer is not reccomended.


#
## Software Requirements
### OS Requirements
This package is supported for *Linux* and *macOS*. The package has been tested on the following systems:
+ Linux: Ubuntu 18.04.6 LTS
+ macOS Monterey 12.5.1

### Python Dependencies
`celigo_pipeline_automation_paper` mainly depends on the Python scientific stack.

```
Jinja2 ~= 3.1.2
Cellprofiler ~= 4.2.4
```

# Installation Guide

There are a few components to this installation guide:
- [Initial Setup](#initial-setup)
- [Package Installation](#package-installation)
- [Ilatik Setup](#ilastik-setup)

## Initial Setup

1. **Install python <=3.9**, [Python Install](https://www.python.org/downloads/)

2. **Make sure git is installed,** [How to install git.](https://git-scm.com/download/win)

3. **Clone Repository,** [How to clone a repository.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) Note: This Process can take 5-10 minutes for a standard computer.
4. **Install make,**  `celigo_pipeline_automation_paper` uses a Makefile to organize its dependencies and development tools. [How to install make.](https://sp21.datastructur.es/materials/guides/make-install.html)

## Package Installation
Once the [Initial Setup](#initial-setup) is complete, navigate to your cloned repository from the command line. Next, you need to build the virtual environment used for running this package. This is done using the Makefile and can be done with the following commands:

    basic usage: `make install`
    development usage: make `make install-dev`

*Note:* This package is dependent on Cellprofiler 4.2.4, which can be a difficult package to install given its many dependencies. We recommend testing the installation of the Cellprofiler package on your computer prior to installing this package. [Cellprofiler Repo](https://github.com/CellProfiler/CellProfiler), [Cellprofiler Package](https://pypi.org/project/CellProfiler/)

## Ilastik Setup
    
1. Install the Ilastik app to your local computer. This can be done from their [website](https://www.ilastik.org/documentation/basics/installation.html). Once you have done this, navigate to the Ilastik app directory and locate the run_ilastik.sh script.

2. Next you will need to manually edit the following in [resource_paths.json](celigo_pipeline_automation_paper/bin/resource_paths.json):

    * "6_well_ilp"  : [Path to 6 Well ILP],
    * "96_well_ilp" : [Path to 96 Well ILP],
    * "run_ilastik" : [Path to run_ilastik.sh]
##
The ILP files can be found under the [pipelines](#celigo_pipeline_automation_paper/pipelines) folder, but are not specifically part of the package. After cloning this repository you can choose to move them to an external location or leave them in place.

Once this process is completed you will want to rerun `make install` or `make install-dev`:
```
make install 
make install-dev
```
# Demos 

## Programmatic Example
```
from celligo_pipeline_automation_paper import CeligoSingleImage

image = CeligoSingleImage(raw_image_path = [RAW_IMAGE_PATH], working_dir = [WORKING_DIRECTORY])

downsample_output_path = image.downsample()
ilastik_output_path = image.run_ilastik()
cellprofiler_output_paths = image.run_cellprofiler()
```
## CLI Example 
The pipeline can also be run from the command line.

#### Single Image
```
celigo_pipeline_cli celigo_pipeline_cli --image_path "[RAW_IMAGE_PATH]" --working_dir "[WORKING_DIRECTORY]"

```
#### Directory
```
run_dir_cli  --dir_path "[RAW_IMAGE_PATH]" --working_dir "[WORKING_DIRECTORY]" --chunk_size [CHUNK_SIZE]

```

# Example Outputs
#### 6 Well
* [6 Well testset](#celigo_pipeline_automation_paper/testset/6_well)
* [6 Well expected output](#celigo_pipeline_automation_paper/testset/6_well_expected_output)
#### 96 Well
* [96 Well testset](#celigo_pipeline_automation_paper/testset/96_well)
* [96 Well expected output](#celigo_pipeline_automation_paper/testset/6_well_expected_output)

# License

This project is covered under the **[Allen Institute Software License](LICENSE)**.

