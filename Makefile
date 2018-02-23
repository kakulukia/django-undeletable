.PHONY: clean-pyc clean-build help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc
	@echo "all clean now .."

clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr htmlcov/
	@rm -fr *.egg-info
	@rm -rf .coverage
	@rm -rf my_secrets

clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.orig' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

init:
	pipenv install --dev
	pipenv shell

init2:
	pipenv install --dev --two
	pipenv shell


lint: ## check style with flake8
	flake8 django_undeletable tests

test: ## run tests quickly with the default Python
	python runtests.py tests

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_undeletable runtests.py tests
	coverage report -m
	coverage html

view-coverage: coverage
	open htmlcov/index.html

release: clean ## package and upload a release (working dir must be clean)
	@while true; do \
		CURRENT=`python -c "import django_secrets; print(django_secrets.__version__)"`; \
		echo ""; \
		echo "=== The current version is $$CURRENT - what's the next one?"; \
		echo "==========================================================="; \
		echo "1 - new major version"; \
		echo "2 - new minor version"; \
		echo "3 - patch"; \
		echo ""; \
		read yn; \
		case $$yn in \
			1 ) bumpversion major; break;; \
			2 ) bumpversion minor; break;; \
			3 ) bumpversion patch; break;; \
			* ) echo "Please answer 1-3.";; \
		esac \
	done
	@python setup.py bdist_wheel && twine upload dist/*
