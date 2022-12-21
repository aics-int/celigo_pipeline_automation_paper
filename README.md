# celigo_pipeline_automation_paper

[![Build Status](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/workflows/Build%20Main/badge.svg)](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/actions)
[![Documentation](https://github.com/BrianWhitneyAI/celigo_pipeline_automation_paper/workflows/Documentation/badge.svg)](https://BrianWhitneyAI.github.io/celigo_pipeline_automation_paper/)
[![Code Coverage](https://codecov.io/gh/BrianWhitneyAI/celigo_pipeline_automation_paper/branch/main/graph/badge.svg)](https://codecov.io/gh/BrianWhitneyAI/celigo_pipeline_automation_paper)

`celigo_pipeline_automation_paper` 

- [Overview](#overview)
- [Documentation](#documentation)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [License](#license)

# Overview
``celigo_pipeline_automation_paper`` is a companion package for [Paper]. It contains algorithms for...


# Documentation

For full package documentation please visit [BrianWhitneyAI.github.io/celigo_pipeline_automation_paper](https://BrianWhitneyAI.github.io/celigo_pipeline_automation_paper).

# System Requirements
## Hardware requirements
`celigo_pipeline_automation_paper` package requires only a standard computer with enough RAM to support the in-memory operations.
#
## Software requirements
### OS Requirements
This package is supported for *Linux*. The package has been tested on the following systems:
+ Linux: Ubuntu 18.04.6 LTS

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

2. **Make sure git is installed.** [How to install git.](https://git-scm.com/download/win)

3. **Clone Repository** [How to clone a repository.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

4. **Install make**  `celigo_pipeline_automation_paper` uses a Makefile to organize its dependencies and development tools. [How to install make.](https://sp21.datastructur.es/materials/guides/make-install.html)

## Package Installation
Once the [Initial Setup](#initial-setup) is complete, navigate to your cloned repository from the command line. Next, you need to build the virtual environment used for running this package. This is done using the Makefile and can be done with the following commands:

    basic usage: `make install`
    development usage: make `make install-dev`

*Note:* This package is dependent on Cellprofiler 4.2.4, which can be a difficult package to install given its many dependencies. We recommend testing the installation of the Cellprofiler package on your computer prior to installing `celigo_pipeline_automation_paper`.

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

Programmatic Example
[pipelines](#celigo_pipeline_automation_paper/pipelines)

CLI Example folder 


# License

This project is covered under the **Allen Institute Software License**.

