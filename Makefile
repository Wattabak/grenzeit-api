SHELL := /bin/bash

usage:
	@echo "Usage:"
	@echo "	usage (default)"
	@echo "	setup_python_interpreter"
	@echo " setup_venv"
	@echo " install_dev_requirements"
	@echo " create_neomodel_migrations"
	@echo " remove_neomodel_migrations"


setup_python_interpreter:
	@pyenv install --skip-existing 3.11.2
	@pyenv local 3.11.2

setup_venv:
	@pyenv exec python3.11 -m venv venv

install_dev_requirements:
	@pip install -r requirements.dev.txt
	@python -m pre-commit install

override NEO4J_USER=neo4j
override NEO4J_PASSWORD=test12345
override NEO4J_HOST=localhost
override NEO4J_PORT=7687

create_neomodel_migrations:
	@neomodel_install_labels 'grenzeit/api/v1/schema.py' \
 		--db 'bolt://$(NEO4J_USER):$(NEO4J_PASSWORD)@$(NEO4J_HOST):$(NEO4J_PORT)'
