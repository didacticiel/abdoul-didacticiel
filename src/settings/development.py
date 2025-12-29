# settings/development.py

from .base import *
from urllib.parse import urlparse 
# Note : 'env' est disponible grâce à 'from .base import *'

# =========================================================================
# 1. PARAMÈTRES DE DÉVELOPPEMENT
# =========================================================================

DEBUG = True # Redéfini pour s'assurer qu'il est True ici

# Hôtes autorisés en dev : Surcharge la liste de base
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    'localhost', '127.0.0.1', '0.0.0.0', 
    urlparse(env('BACKEND_DOMAIN', default='')).netloc
])

# Autoriser toutes les origines CORS en dev
CORS_ALLOW_ALL_ORIGINS = True

# --- AJUSTEMENTS DE LA BASE DE DONNÉES ---
# Si vous avez besoin de forcer des options spécifiques en dev:

# Assurez-vous que l'hôte de la DB est toujours lu du .env ou par défaut 'localhost'
DATABASES['default']['HOST'] = env('DATABASE_HOST', default='localhost')

# Désactiver SSL en mode dev (si l'option existe déjà dans base.py)
if 'OPTIONS' not in DATABASES['default']:
    DATABASES['default']['OPTIONS'] = {}
if 'sqlite' in DATABASES['default']['ENGINE']:
    # SQLite ne supporte AUCUNE option SSL, on vide le dictionnaire OPTIONS
    DATABASES['default']['OPTIONS'] = {}


# ⭐ FIX COOKIE ADMIN 
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False 


# =========================================================================
# 2. DEBUG TOOLBAR
# =========================================================================

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
# Assurez-vous que le middleware est ajouté en PREMIER après Security/WhiteNoise
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
INTERNAL_IPS = ['127.0.0.1']