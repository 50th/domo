#!/usr/bin/bash

python manage.py makemigrations
python manage.py migrate
gunicorn -c gunicorn_conf.py domo.wsgi:application
