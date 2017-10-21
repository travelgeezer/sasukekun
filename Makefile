ENV = pipenv run
EXECUTE = $(ENV) python manage.py

run:
		/usr/local/bin/pipenv run gunicorn --workers=2 --bind unix:/home/ubuntu/sasukekun/sasukekun.sock growth_studio.wsgi
dev:
		$(EXECUTE) runserver

publish:
		$(ENV) fab deploy -H sasukekun.cn --user ubuntu

.PHONY: run dev publish

