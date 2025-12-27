#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Lancer les tests
python manage.py test --settings=src.settings.testing

# 3. Collecte des fichiers statiques
python manage.py collectstatic --no-input --settings=src.settings.production

# 4. Mise à jour de la base de données
python manage.py migrate --settings=src.settings.production

# 5. Création automatique du Superuser (L'ajout est ici !)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Création du superutilisateur..."
    python manage.py createsuperuser \
        --no-input \
        --settings=src.settings.production || echo "Le superutilisateur existe déjà ou erreur lors de la création."
fi

# 6. Démarrage
echo "Démarrage de Gunicorn..."
exec gunicorn src.wsgi:application --bind 0.0.0.0:8000