#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py test --settings=src.settings.testing
python manage.py collectstatic --no-input --settings=src.settings.production
python manage.py migrate --settings=src.settings.production

echo "Démarrage de Gunicorn..."
exec gunicorn src.wsgi:application --bind 0.0.0.0:8000
# fin