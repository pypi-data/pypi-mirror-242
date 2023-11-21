.PHONY: all
all: help

## - format
##	Automatically run black linting and isort sorting.
.PHONY: format
format: isort lint

## - format-check
##	Check (but don't apply) black linting and isort sorting.
.PHONY: format-check
format-check: lint-check isort-check

## - lint
##	Automatically format project code with black.
.PHONY: lint
lint:
	black .

## - lint-check
##	Check linting of code with black.
.PHONY: lint-check
lint-check:
	black . --diff --color --check

## - isort
##	Automatically sort imports in project code using isort.
.PHONY: isort
isort:
	isort .

## - isort-check
##	Check sorting of imports in project code using isort.
.PHONY: isort-check
isort-check:
	isort . --diff --color --check

## - test
##	Run pytest tests.
.PHONY: test
test:
	python -m pytest

## - test-cov
##	Run pytest tests with coverage report.
.PHONY: test-cov
test-cov:
	python -m pytest --cov=poglink --cov-report=xml:coverage.xml
	@coverage report
	@coverage html

## - clean
##	Clean all build directories.
.PHONY: clean
clean: clean-python
	rm -f coverage.xml .coverage

## - clean-python
##	Clean python build directory.
.PHONY: clean-python
clean-python:
	rm -rfv dist/*

## - python-build
##	Build python source distribution (tarball).
.PHONY: python-build
python-build: clean-python
	python -m build

## - python-publish-test
##	Publish python package to test.pypi.org.
.PHONY: python-publish-test
python-publish-test: python-build
	scripts/python-publish.sh

## - python-publish-prod
##	Publish python package to pypi.org.
.PHONY: python-publish-prod
python-publish-prod: python-build
	PROD=true scripts/python-publish.sh

## - docker-build
##	Build docker image.
.PHONY: docker-build
docker-build:
	scripts/docker-build.sh

## - help:
##	Show this help text.
.PHONY: help
help:
	@sed -n 's/^##//p' $(MAKEFILE_LIST)
