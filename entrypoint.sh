#!/usr/bin/env bash
python manage.py db upgrade
flask run --host=0.0.0.0 --port=3111