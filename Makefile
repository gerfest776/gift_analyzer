.PHONY: mmigr migrate run test db

mmigr:
		python manage.py makemigrations

migrate:
		python manage.py migrate

run:
		python manage.py runserver

test:
		python manage.py test

db:
		docker-compose up -d db
