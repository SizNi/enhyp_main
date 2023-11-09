#!/bin/sh

# Выполняем миграции
python src/manage.py makemigrations
python src/manage.py migrate
# python src/manage.py runserver 0.0.0.0:8000
python src/manage.py collectstatic
gunicorn --workers=4 --bind=127.0.0.1:8000 --chdir ./src/ config.wsgi:application