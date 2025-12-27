# settings/production.py

from .base import *

# =========================================================================
# 1. SÉCURITÉ & HÔTES
# =========================================================================

DEBUG = False
# Doit être défini via env.list('ALLOWED_HOSTS')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS') 

# CORS : Doit être restrictif en production, listant uniquement le domaine frontend/backend
# L'importation de 'env' est gérée par 'from .base import *'
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_ALL_ORIGINS = False 


# =========================================================================
# 2. SESSIONS & COOKIES (HTTPS REQUIS)
# =========================================================================

# Le paramètre 'None' nécessite absolument 'Secure = True' pour les requêtes cross-site (JWT)
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None" 

# Les cookies JWT doivent aussi être sécurisés en production
JWT_COOKIE_SECURE = True # Surcharge la valeur de base (qui peut être False en dev)
JWT_COOKIE_SAMESITE = "None" 

# =========================================================================
# 3. SÉCURITÉ HTTPS (HSTS, REDIRECTION)
# =========================================================================

# Indique à Django que le proxy (Nginx/Render/Heroku) utilise HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Redirige tout le trafic HTTP vers HTTPS
# Laisse Render gérer la redirection HTTP vers HTTPS pour le moment
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000        # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =========================================================================
# 4. BASE DE DONNÉES & CACHE
# =========================================================================

# Si vous utilisez un service cloud, vous devriez exiger SSL
DATABASES['default']['OPTIONS']['sslmode'] = 'require'

# Utiliser Redis en Production
CACHES = {
    'default': env.cache('REDIS_URL', default='redis://127.0.0.1:6379/1')
}

# Utiliser le backend email réel (si non défini dans .env, il prendra la console)
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')


# =========================================================================
# 5. NETTOYAGE DES OUTILS DE DEV
# =========================================================================

# Nettoyage des applications non désirées en production
PRODUCTION_APPS_EXCLUDE = ['debug_toolbar', 'rosetta', 'django_extensions']
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in PRODUCTION_APPS_EXCLUDE]

# Nettoyage des middlewares de debug
PRODUCTION_MIDDLEWARE_EXCLUDE = ['debug_toolbar.middleware.DebugToolbarMiddleware']
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in PRODUCTION_MIDDLEWARE_EXCLUDE]