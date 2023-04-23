PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

install:
	poetry install

build:
	poetry build

start:
	poetry run python3 manage.py runserver

shell:
	poetry run python manage.py shell

lint:
	poetry run flake8 task_manager
