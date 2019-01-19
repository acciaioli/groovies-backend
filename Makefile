.PHONY: clean clean-test clean-pyc help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

clean-test: ## remove test and coverage artifacts
	rm -f backend/.coverage \
	rm -fr backend/htmlcov/ \
	rm -fr .mypy_cache \

create-keys: ## creates a rsa key pair
	cd backend && j-crypto-create-pair backend && cd ..
lint: # check style with flake8
	flake8 backend

type-check: ## check types with mypy
	mypy backend && rm -r .mypy_cache

migrations-check: # checks models consistency
	cd backend && python manage.py makemigrations --check --dry-run && cd ..

test: # run django tests with coverage
	cd backend && coverage run manage.py test -v 2 && coverage html && cd ..

codecov:
	cd backend && codecov

run-tests:
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) migrations-check
	$(MAKE) test

run-ci:
	$(MAKE) create-keys
	$(MAKE) run-tests
	$(MAKE) codecov

start-dev: # start development containers
	docker-compose build
	docker-compose run --rm -p 8000:8000 web bash -c "bash"
	docker-compose down
