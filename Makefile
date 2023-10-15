# VARIABLES
#------------------------------------------
MANAGE = python manage.py

# BASE COMMANDS
run:
	$(MANAGE) init_project
	$(MANAGE) runserver


run-local:
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput
	$(MANAGE) init_project
	python manage.py runserver 0.0.0.0:8000


# DB
migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

reset:
	$(MANAGE) reset_db

mm:
	$(MANAGE) makemigrations
	$(MANAGE) migrate


# Docker
local_up:
	sudo docker compose up --build

local_down:
	sudo docker compose down


