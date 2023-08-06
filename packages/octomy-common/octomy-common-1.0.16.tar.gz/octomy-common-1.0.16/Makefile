.SUFFIXES: .js .css .html .svg .jpeg .png .htm
.PHONY: all code-quality test setup up req

.EXPORT_ALL_VARIABLES:
SHELL:=/bin/bash

DOCKER_BUILDKIT:=1

ROOT_DIR:=$(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")
TESTS_DIR:=${ROOT_DIR}/tests
REQUIREMENTS_DIR:=${ROOT_DIR}/requirements
CODE_QUALITY_DIR:=${ROOT_DIR}/code_quality
FK_BARE_VERSION:=$(shell cat "$(ROOT_DIR)/VERSION")

CI_COMMIT_REF_NAME?=$(shell git rev-parse --abbrev-ref HEAD)
FK_GIT_ACTUAL_BRANCH:=$(CI_COMMIT_REF_NAME)
FK_GIT_HASH?=$(shell git rev-parse HEAD)
FK_GIT_HASH_SHORT?=$(shell git rev-parse --short HEAD)
FK_BUILD_DATE=?=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

# See https://gitlab.com/octomy/common#versioning for details on versioning scheme
FK_VERSION:=$(shell \
	branch=$(FK_GIT_ACTUAL_BRANCH); \
	version='$(FK_BARE_VERSION)'; \
	if [[ "$${branch}" == production ]]; then \
		echo "$${version}"; \
	elif [[ "$${branch}" == beta ]]; then \
		echo "$${version}-beta"; \
	elif [[ "$${branch}" == stage-* ]] && [[ "$${branch:6}" != "" ]] ; then \
		echo "$${version}-$${branch:6}"; \
	else \
		echo "$${version}-test-$${branch//[      ]/_}"; \
	fi )
	

VENV_NAME:=fk_venv

FK_PROJECT_GROUP_BASE_NAME:=octomy
FK_PROJECT_BASE_NAME:=common
FK_PROJECT_NAME:=$(FK_PROJECT_GROUP)/$(FK_PROJECT_BASE_NAME)

FK_DOCKER_REGISTRY_NAME:=${FK_DOCKER_REGISTRY_NAME}
FK_DOCKER_REGISTRY_FILENAME:=$(FK_DOCKER_REGISTRY_NAME)_credentials.yaml
FK_DOCKER_REGISTRY_DOMAIN:=${FK_DOCKER_REGISTRY_DOMAIN}
FK_DOCKER_REGISTRY_URL:=https://$(FK_DOCKER_REGISTRY_DOMAIN)
FK_DOCKER_REGISTRY_PROJECT_URL:=$(FK_DOCKER_REGISTRY_URL)/$(FK_PROJECT_GROUP_BASE_NAME)
FK_DOCKER_REGISTRY_PROJECT_DOMAIN:=$(FK_DOCKER_REGISTRY_DOMAIN)/$(FK_PROJECT_GROUP_BASE_NAME)
FK_DOCKER_REGISTRY_USERNAME:=${FK_DOCKER_REGISTRY_USERNAME}
FK_DOCKER_REGISTRY_PASSWORD:=${FK_DOCKER_REGISTRY_PASSWORD}

FK_PYPI_REGISTRY_URL_BASE:=gitlab.com/api/v4/projects/23170380/packages/pypi/simple
FK_PYPI_REGISTRY_USERNAME:=__token__
FK_PYPI_REGISTRY_PASSWORD:=${FK_PYPI_TOKEN}
FK_PYPI_REGISTRY_URL:=https://$(FK_PYPI_REGISTRY_USERNAME):$(FK_PYPI_REGISTRY_PASSWORD)@$(FK_PYPI_REGISTRY_URL_BASE)


FK_NAMESPACE:=merchbot-$(FK_GIT_ACTUAL_BRANCH)


GITLAB_CACHE_DIR:=$(shell pwd)/gitlab_cache



define twine_config
[distutils]
index-servers=pypi
[pypi]
username=__token__
password=${TWINE_TOKEN}
endef
export twine_config


all: help

info:
	@echo "ROOT_DIR=$(ROOT_DIR)"
	@echo "FK_BARE_VERSION=$(FK_BARE_VERSION)"
	@echo "FK_VERSION=$(FK_VERSION)"
	@echo "TESTS_DIR=$(TESTS_DIR)"
	@echo "REQUIREMENTS_DIR=$(REQUIREMENTS_DIR)"
	@echo "CODE_QUALITY_DIR=$(CODE_QUALITY_DIR)"
	@echo "FK_GIT_ACTUAL_BRANCH=$(FK_GIT_ACTUAL_BRANCH)"
	@echo "CI_COMMIT_REF_NAME=$(CI_COMMIT_REF_NAME)"
	@echo "CI_COMMIT_TAG=$(CI_COMMIT_TAG)"
	@echo "CI_PROJECT_DIR=$(CI_PROJECT_DIR)"
	@echo "GITLAB_CACHE_DIR=$(GITLAB_CACHE_DIR)"
	@echo "VENV_NAME=$(VENV_NAME)"

env:
	@echo "=== ENV"
	export -p
	@echo " "

ver:
	@echo "=== DOCKER TAG / PYPI VERSION:"
	@echo "$(FK_VERSION)"
	@echo " "
	@echo "=== OS:"
	@cat '/etc/os-release'
	@echo " "
	@echo "=== PYTHON & PIP:"
	@. ~/.venv/$(VENV_NAME)/bin/activate;\
	 python --version || python3 --version || echo "NO PYTHON";\
	 pip --version || pip3 --version || echo "NO PIP"
	@echo " "
	@echo "=== DOCKER:"
	@docker --version || echo "NO DOCKER"
	@echo " "
	@echo "=== DOCKER-COMPOSE:"
	@docker-compose --version || echo "NO DOCKER-COMPOSE"
	@echo " "
	@echo "=== KUBECTL:"
	@kubectl version --client || echo "NO KUBECTL"
	@echo " "
	@echo "=== GCLOUD:"
	@gcloud --version || echo "NO GCLOUD"
	@echo " "
	@echo "=== WHICH:"
	@which docker || echo "NO WHICH DOCKER"
	@which docker-compose || echo "NO WHICH DOCKER-COMPOSE"
	@which kubectl || echo "NO WHICH KUBECTL"
	@which gcloud || echo "NO WHICH GCLOUD"
	@echo " "

# Python requirements management
###################################################################

req-prep:
	pip install --upgrade pip pip-tools

req-src:
	cd "$(REQUIREMENTS_DIR)"; \
	pip-compile --no-header --no-emit-index-url --output-file=requirements.txt \
		requirements.in; \
	pip-compile --no-header --no-emit-index-url --output-file=test_requirements.txt \
		requirements.in \
		test_requirements.in; \

req-install:
	cd "$(REQUIREMENTS_DIR)"; \
	pip install -r requirements.txt

req-install-test:
	cd "$(REQUIREMENTS_DIR)"; \
	pip install -r test_requirements.txt

req: req-prep req-src

uninstall:
	pip uninstall -y octomy-common;

test:
	cd "${TESTS_DIR}" && make all || echo "OOOPS"

code-quality:
	cd code_quality; \
	make all


# Build and re-install package locally
setup: uninstall
	FK_GIT_ACTUAL_BRANCH=$(FK_GIT_ACTUAL_BRANCH) pip install -e $(ROOT_DIR);

pypi-build:
	FK_GIT_ACTUAL_BRANCH=$(FK_GIT_ACTUAL_BRANCH) python setup.py build --parallel 99
	FK_GIT_ACTUAL_BRANCH=$(FK_GIT_ACTUAL_BRANCH) python setup.py sdist bdist_wheel
	ls -halt dist/

pypi-push:
	echo "$$twine_config" > 'twine.conf'
	twine upload --config-file twine.conf dist/*.tar.gz --skip-existing --verbose
	rm 'twine.conf'

pypi-push-local:
	@echo "Pushing using username and pass"
	twine upload dist/*.tar.gz --skip-existing --verbose


help:
	@echo ""
	@echo " Convenience makefile for FK tools"
	@echo " ---------------------------------"
	@echo ""
	@echo "  Preparation:"
	@echo ""
	@echo "    make pypi-build          - Build and pack into PyPi package"
	@echo "    make pypi-push           - Push the package to PyPi"
	@echo "    make pypi-push-local     - Push the package to PyPi using manual entry of credentials"
	@echo ""
	@echo "  Information output:"
	@echo ""
	@echo "    make ver                 - Lists current tool versions"
	@echo "    make info                - Lists internal variables"
	@echo "    make env                 - Lists environment variables"
	@echo "    make req                 - Rebuild pinned versions in *requirements.txt from *requirements.in"
	@echo "    make test                - Run tests. NOTE: For more options see tests/Makefile"
	@echo ""
	@echo "  Code quality:"
	@echo ""
	@echo "    make code-quality        - Run all code quality checks. NOTE: For more options see code_quality/Makefile"
