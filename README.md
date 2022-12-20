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
``celigo_pipeline_automation_paper`` 


# Documentation

For full package documentation please visit [BrianWhitneyAI.github.io/celigo_pipeline_automation_paper](https://BrianWhitneyAI.github.io/celigo_pipeline_automation_paper).

# System Requirements
## Hardware requirements
`celigo_pipeline_automation_paper` package requires only a standard computer with enough RAM to support the in-memory operations.

## Software requirements
### OS Requirements
This package is supported for *Linux*. The package has been tested on the following systems:
+ Linux: Ubuntu 16.04

### Python Dependencies
`celigo_pipeline_automation_paper` mainly depends on the Python scientific stack.

```
Jinja2 ~= 3.1.2
Cellprofiler ~= 4.2.4
```

# Installation Guide

### Pre-requisites
Python 3.9 & `make`
#
## Package Installation

baisc usage: `make install`
development usage: make `make install-dev`

*Note:* This package is dependent on Cellprofiler 4.2.4, which can be a diffacult package to install given it's many dependencies, we reccomend testing the install of the Cellprofiler package on your computer prior to installing `celigo_pipeline_automation_paper`.

## Ilastik Setup
    
1. Install the Ilastik app to your local computer. This can be done from their [website](https://www.ilastik.org/documentation/basics/installation.html). Once you have done this, navigate to the Ilastik app folder and locate the run_ilastik.sh script.

2. Next you will need to manually edit the following in [resource_paths.json](celigo_pipeline_automation_paper/bin/resource_paths.json):

    * "6_well_ilp"  : [Path to 6 Well ILP],
    * "96_well_ilp" : [Path to 96 Well ILP],
    * "run_ilastik" : [Path to run_ilastik.sh]
##
The ILP files can be found under the [pipelines](#celigo_pipeline_automation_paper/pipelines) folder, but are not specifically part of the package, After cloning this repository you can choose to move them to an external location or leave them in place.
##
Once this process is completed you will want to rerun `make install`

# Demos 

Programatic Example
[pipelines](#celigo_pipeline_automation_paper/pipelines)

CLI Example folder 


# License

This project is covered under the **Allen Institute Software License**.

