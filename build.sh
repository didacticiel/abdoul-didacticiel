# abdoul-didacticiel/build.sh
#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installation des dépendances
pip install -r requirements.txt

# 2. VÉRIFICATION : Lancer les tests avant de continuer
# On utilise SQLite en mémoire pour que les tests soient rapides sur Render
python manage.py test --settings=src.settings.testing

# 3. Collecte des fichiers statiques
python manage.py collectstatic --no-input --settings=src.settings.production

# 4. Mise à jour de la base de données PostgreSQL
python manage.py migrate --settings=src.settings.production

# 5. DÉMARRAGE DU SERVEUR (Indispensable !)
echo "Démarrage de Gunicorn..."
exec gunicorn src.wsgi:application --bind 0.0.0.0:8000