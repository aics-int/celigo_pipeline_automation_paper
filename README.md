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

# Installation

## Installation Guide
#### Pre-requisites
Python 3.10 & `make`

## Package install
    baisc usage: `make install`
    development usage: make `make install-dev`

## Ilastik Setup
    https://www.ilastik.org/documentation/basics/installation.html

## Configuring resource_paths.json
    You will need to manually edit the following:

    "6_well_ilp":"/allen/aics/microscopy/CellProfiler_4.1.3_Testing/6WellCeligoPipelines/6_well_colony_ilastikpipeline_v2.1.1.ilp",
    "96_well_ilp": "/allen/aics/microscopy/CellProfiler_4.1.3_Testing/96wellPipeline_v2/96_well_colony_celigo_v2.ilp",
    "run_ilastik": "/allen/aics/apps/prod/ilastik/ilastik-1.3.3post3-Linux/run_ilastik.sh"

# Demos 

Programatic Example


CLI Example folder 


# License

This project is covered under the **Allen Institute Software License**.

