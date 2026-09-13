#!/bin/bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create superuser if it doesn't already exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'cmucuio@gmail.com', 'Kimberley#2026!Reporta!')
    print('Superuser created')
else:
    print('Superuser already exists')
"