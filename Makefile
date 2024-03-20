serve:
	python3 manage.py runserver
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
develop:
	python manage.py runserver_plus --cert-file cert.crt
sync:
	python3 manage.py migrate --run-syncdb 
build:
	docker-compose -f docker-compose.dev.yml up --build
kill:
	sudo fuser -k 8000/tcp
