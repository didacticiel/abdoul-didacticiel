#!/usr/bin/env bash
# LOGIQUE : Ce script contient les commandes manuelles que tu devrais taper
# pour installer ton site sur un nouvel ordinateur.

set -o errexit # Arrête tout si une commande échoue (évite de déployer un site cassé)

# 1. Installation des bibliothèques Python (Gunicorn, Whitenoise, etc.)
pip install -r requirements.txt

# 2. Collecte des fichiers statiques (CSS, JS, Images)
# Whitenoise va les compresser pour qu'ils se chargent plus vite en ligne.
python manage.py collectstatic --no-input --settings=src.settings.production

# 3. Mise à jour de la base de données PostgreSQL
# Applique tes modèles (User, Project, Contact) sur la DB de Render.
python manage.py migrate --settings=src.settings.production