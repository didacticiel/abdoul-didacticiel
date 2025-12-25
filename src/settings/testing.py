# settings/testing.py

from .base import *

# =========================================================================
# 1. PARAMÈTRES GÉNÉRAUX
# =========================================================================

DEBUG = False 
ALLOWED_HOSTS = ['testserver'] 

# =========================================================================
# 2. BASE DE DONNÉES (Utiliser SQLite en mémoire pour la vitesse)
# =========================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:', # DB en mémoire (très rapide)
    }
}

# =========================================================================
# 3. CACHE ET ASYNCHRONE (Désactiver les dépendances externes)
# =========================================================================

# Utiliser le cache local en mémoire au lieu de Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-test-key',
    }
}

# Envoyer les emails dans une liste de mémoire (pour vérification)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Désactiver Celery pendant les tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# =========================================================================
# 4. SÉCURITÉ ET AUTRES
# =========================================================================

# Clé secrète de test
SECRET_KEY = env('SECRET_KEY')

# Assurer que les applications de debug ne sont pas chargées
TESTING_APPS_EXCLUDE = ['debug_toolbar']
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in TESTING_APPS_EXCLUDE]

# Assurer que les middlewares de debug sont retirés
TESTING_MIDDLEWARE_EXCLUDE = ['debug_toolbar.middleware.DebugToolbarMiddleware']
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in TESTING_MIDDLEWARE_EXCLUDE]