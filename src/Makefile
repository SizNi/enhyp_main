dev:
	python3 manage.py runserver
	
install:
	poetry install

start:
	gunicorn --workers=4 --bind=127.0.0.1:8000 config.wsgi:application

new_app:
	#django-admin startapp app_name

# линтеры
lint:
	poetry run flake8

black:
	black .

# тесты
test:
	python3 manage.py test

pytest:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

# миграции
create_model:
	python manage.py makemigrations

migration:
	python manage.py sqlmigrate {app_name} 0001

commit_migration:
	python manage.py migrate

# создание пакетов для различных языков
trans:
	django-admin makemessages -l en_us

compile:
	django-admin compilemessages

# старт серверов базы данных
dbstart:
	sudo service postgresql start

vue:
	cd form && npm install && npm run build

container:
	cd .. &&docker build -t enhyp-app .

run_container:
	docker run -it --name enhyp enhyp-app /bin/bash

docker_rebuild:
	docker compose down && docker compose up --build

docker_nocache:
	docker compose build --no-cache