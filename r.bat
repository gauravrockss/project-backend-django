@echo off
call venv\Scripts\activate

set DJANGO_ENV=development
python manage.py runserver