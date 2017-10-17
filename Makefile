run:
		/usr/local/bin/pipenv run gunicorn --workers=2 --bind unix:/home/ubuntu/sasukekun/sasukekun.sock growth_studio.wsgi

.PHONY: run

