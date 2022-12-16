# See https://tech.davis-hansson.com/p/make/
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

##############################################

PYTHON_VERSION = python3
VENV_NAME := venv
VENV_BIN := $(VENV_NAME)/bin
ACTIVATE = $(VENV_BIN)/activate
PYTHON = $(VENV_BIN)/python3

$(PYTHON):
> test -d $(VENV_NAME) || $(PYTHON_VERSION) -m venv --upgrade-deps $(VENV_NAME)

venv: $(PYTHON)

install: venv
> $(PYTHON) -m pip install --index-url='https://artifactory.corp.alleninstitute.org/artifactory/api/pypi/pypi-virtual/simple' --extra-index-url='https://artifactory.corp.alleninstitute.org/artifactory/api/pypi/pypi-snapshot-local/simple' . 
.PHONY: install

install-dev: venv install
> $(PYTHON) -m pip install .[dev]
> $(VENV_BIN)/pre-commit install
.PHONY: install-dev

lint:
> $(PYTHON) -m flake8 --count --show-source --statistics celigo_pipeline_automation_paper
.PHONY: lint

type-check:
> $(PYTHON) -m mypy --ignore-missing-imports  celigo_pipeline_automation_paper
.PHONY: type-check

fmt:
> $(PYTHON) -m black celigo_pipeline_automation_paper
.PHONY: fmt

import-sort:
> $(PYTHON) -m isort celigo_pipeline_automation_paper
.PHONY: import-sort

test:
> $(PYTHON) -m pytest celigo_pipeline_automation_paper/tests/
.PHONY: test

test-exclude-slow:
> $(PYTHON) -m pytest -m "not slow"
.PHONY: test-exclude-slow

clean:  # Clear proj dir of all .gitignored files
> git clean -Xfd -e "!.vscode"
.PHONY: clean

