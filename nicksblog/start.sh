#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn --access-logfile - nicksblog.wsgi -b :8000
