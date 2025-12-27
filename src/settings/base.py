# settings/base.py
import sys
import os
from pathlib import Path
from datetime import timedelta
import environ
from django.contrib import admin

# Logique : Configuration d'Environ
env = environ.Env()
# Lit le fichier .env (s'il existe)
environ.Env.read_env(str(Path(__file__).resolve().parent.parent.parent / '.env'))

# =========================================================================
# 1. CHEMINS & ENVIRONNEMENT
# =========================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# Quick-start development settings - unsuitable for production

# Récupération des variables d'environnement
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dummy-key-for-ci')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# =========================================================================
# 2. APPLICATIONS
# =========================================================================

DJANGO_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
# ... (inchangé)
    # API & JWT
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    # Utilitaires & Outils
    'corsheaders',
    'django_filters',
    'django_extensions',
    'easy_thumbnails',
    'django_redis',
    'ckeditor', 
    'ckeditor_uploader',
    # 💡 AJOUT : Support HTMX
    'django_htmx', 
    
    # Authentification (Nous gardons le minimum pour l'email, mais retirons dj_rest_auth/allauth car nous utilisons JWT)
    'allauth',
    'allauth.account', 
    
    # Retrait de dj_rest_auth/dj_rest_auth.registration, rosetta, drf_spectacular (pour l'instant)
]

LOCAL_APPS = [

    'apps.core',
    'apps.users',
    'apps.blog',
    'apps.portfolio',
   
  
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# =========================================================================
# 3. MIDDLEWARE
# =========================================================================

MIDDLEWARE = [
# ... (inchangé)
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    
    # Middleware HTMX
    'django_htmx.middleware.HtmxMiddleware', 
    
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
     
]

ROOT_URLCONF = 'src.urls'


# =========================================================================
# 4. TEMPLATES & WSGI
# =========================================================================

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Utiliser BASE_DIR / 'templates'
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'



# =========================================================================
# 5. BASE DE DONNÉES (Configuration avec repli sécurisé)
# =========================================================================
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DATABASE_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': env('DATABASE_USER', default=''),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default='localhost'), 
        'PORT': env.int('DATABASE_PORT', default=5432),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
    }
}

# Modèle Utilisateur Personnalisé
AUTH_USER_MODEL = 'users.User'


# Validation des Mots de Passe
AUTH_PASSWORD_VALIDATORS = [
# ... (inchangé)
    # ... Vos validateurs existants ...
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================================
# 6. INTERNATIONALISATION & SITES
# =========================================================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = env('TIME_ZONE', default="Africa/Porto-Novo")
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

SITE_ID = 1

# Configuration allauth (gardée pour la gestion email/token si nécessaire)

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_METHODS = ['email']  # Utilisation d'une liste
#  CORRECTION: Utiliser 'username' ou retirer la ligne si vous utilisez seulement une vue DRF personnalisée.
#ACCOUNT_SIGNUP_FIELDS = ['username'] 
SOCIALACCOUNT_AUTO_SIGNUP = True
# Cherche la section 6 (INTERNATIONALISATION & SITES)
# Remplace par cette configuration cohérente :

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False      # Désactive le besoin d'un username
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # Indique qu'il n'y a pas de champ username
ACCOUNT_EMAIL_VERIFICATION = 'none'




# =========================================================================
# 7. DJANGO REST FRAMEWORK & JWT
# =========================================================================

#  RETRAIT DE REST_AUTH (Nous utilisons Simple JWT directement)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
        'rest_framework.authentication.SessionAuthentication', # Gardé pour l'admin
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/min',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Cookies JWT HttpOnly (Renommés)
JWT_COOKIE_NAME = "abdoul_didacticiel_jwt"
JWT_REFRESH_COOKIE_NAME = "abdoul_didacticiel_jwt_refresh"
JWT_COOKIE_SECURE = env.bool('JWT_COOKIE_SECURE', default=False) 
JWT_COOKIE_SAMESITE = "Lax"    
JWT_COOKIE_HTTPONLY = True


# =========================================================================
# 8. FICHIERS STATIQUES, MÉDIAS & EMAIL
# =========================================================================

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Répertoire de déploiement
STATICFILES_DIRS = [
    #BASE_DIR / 'apps/static', # Répertoire de développement (où NPM génère styles.css)
    BASE_DIR / 'static', # Répertoire de développement (où NPM génère styles.css)
]

# On n'utilise le stockage compressé de WhiteNoise QUE si DEBUG est False (en production)
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # En développement, on laisse Django gérer ça normalement
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@abdouldidacticiel.bj')

# Logging 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # (handlers et loggers)
}


# =========================================================================
# 9. CONFIGURATION CKEDITOR
# =========================================================================

CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/" # Chemin dans MEDIA_ROOT

CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'full', # Utilisez la barre d'outils que vous préférez
        'skin': 'moono-lisa', # ou 'moono'
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'Source'],
        ],
        'extraPlugins': 'codesnippet', # Si vous voulez des blocs de code
    }
}


# =========================================================================
# 10. AUTHENTIFICATION SOCIALE (GOOGLE)
# =========================================================================
GOOGLE_OAUTH_CLIENT_ID = env('GOOGLE_OAUTH_CLIENT_ID', default='')
GOOGLE_OAUTH_CLIENT_SECRET = env('GOOGLE_OAUTH_CLIENT_SECRET', default='')


#  CORRECTION: Ajout pour résoudre models.W042
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'