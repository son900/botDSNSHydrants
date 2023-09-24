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
	$(MANAGE) runserver


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


