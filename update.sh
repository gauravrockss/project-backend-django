#!/bin/bash

# Activate the virtual environment
source venv/bin/activate
export DJANGO_ENV=production

git pull

pip install -r requirements.txt

# Run your command
nohup python manage.py runserver 8001 &
