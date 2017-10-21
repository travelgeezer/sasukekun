EXECUTE = pipenv run python manage.py

run:
		/usr/local/bin/pipenv run gunicorn --workers=2 --bind unix:/home/ubuntu/sasukekun/sasukekun.sock growth_studio.wsgi
dev:
		$(EXECUTE) runserver

.PHONY: run dev

