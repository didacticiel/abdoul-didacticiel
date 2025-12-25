#settings/base.py
import sys
import os
from pathlib import Path
from datetime import timedelta
import environ
from django.contrib import admin

# =========================================================================
# 1. CHEMINS & ENVIRONNEMENT
# =========================================================================

# Logique : Définit le répertoire de base du projet.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Logique : Initialisation de django-environ pour gérer les variables d'environnement.
env = environ.Env(
    # DEBUG est False par défaut pour la sécurité. Sera True dans development.py.
    DEBUG=(bool, False),
    USE_TZ=(bool, True),
    BACKEND_DOMAIN=(str, 'http://localhost:8000'),
    
    # Configuration Google pour la méthode ID Token
    GOOGLE_OAUTH_CLIENT_ID=(str, 'VOTRE_CLIENT_ID_GOOGLE_DEV'),
    GOOGLE_OAUTH_CLIENT_SECRET=(str, 'VOTRE_SECRET_GOOGLE_DEV'),
    
    FRONTEND_URL=(str, 'http://localhost:8080'), 
)

# Lecture du fichier .env
environ.Env.read_env(BASE_DIR / '.env')

# --- Variables de Sécurité & Base ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG') # Lu depuis le .env (ou False par défaut)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# --- Variables FedaPay ---
FEDAPAY_SANDBOX_MODE = env.bool('FEDAPAY_SANDBOX_MODE', default=True)
# Les clés elles-mêmes, lues directement.
FEDAPAY_ENVIRONMENT = env('FEDAPAY_ENVIRONMENT', default='sandbox')

# Définir l'URL de l'API en fonction de l'environnement (Sandbox ou Live)
if FEDAPAY_ENVIRONMENT == 'sandbox':
    FEDAPAY_API_URL = 'https://sandbox-api.fedapay.com/v1'
else:
    FEDAPAY_API_URL = 'https://api.fedapay.com/v1'
    
FEDAPAY_SECRET_KEY = env('FEDAPAY_SECRET_KEY')
FEDAPAY_PUBLIC_KEY = env('FEDAPAY_PUBLIC_KEY')
FEDAPAY_WEBHOOK_SECRET = env('FEDAPAY_WEBHOOK_SECRET')
# Récupérer la variable BACKEND_DOMAIN
BACKEND_DOMAIN = env('BACKEND_DOMAIN')
if BACKEND_DOMAIN and 'ngrok' in BACKEND_DOMAIN:
    # Extrait '619c6ca0514d.ngrok-free.app' de 'https://619c6ca0514d.ngrok-free.app'
    try:
        from urllib.parse import urlparse
        host_from_domain = urlparse(BACKEND_DOMAIN).netloc
        if host_from_domain not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host_from_domain)
    except ImportError:
        pass # Ignorer si urlparse n'est pas disponible (improbable)
FEDAPAY_CALLBACK_URL = env('FEDAPAY_CALLBACK_URL', default=f'{BACKEND_DOMAIN}/api/v1/payments/webhook/')
FEDAPAY_RETURN_URL = env('FEDAPAY_RETURN_URL', default=f'{BACKEND_DOMAIN}/payments/return/')
# Variables d'environnement pour l'accès aux services externes
GOOGLE_OAUTH_CLIENT_ID = env('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = env('GOOGLE_OAUTH_CLIENT_SECRET')
FRONTEND_URL = env('FRONTEND_URL')
BACKEND_DOMAIN = env('BACKEND_DOMAIN') 

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
    # REST Framework & JWT
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Outils
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    
    # Authentification (Nous gardons le minimum pour les fonctionnalités email)
    'allauth',
    'allauth.account', 
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    # Utilitaires
    'easy_thumbnails',
    'django_redis',
    'django_extensions',
    'rosetta',
]
LOCAL_APPS = [
    'apps.cv_app',
    'apps.users',
    'apps.payments',   
    
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Logique : Indique à Django quel modèle utiliser pour l'authentification.
AUTH_USER_MODEL = 'users.User' 

# =========================================================================
# 3. MIDDLEWARE & URLS
# =========================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
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

ROOT_URLCONF = 'CvDidacticiel_API.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'CvDidacticiel_API.wsgi.application'


# =========================================================================
# 4. BASE DE DONNÉES & CACHE
# =========================================================================

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST', default='localhost'), 
        'PORT': env('DATABASE_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            # 'sslmode': 'require',  # si using SSL
            'connect_timeout': 5,
        },
    }
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'cvdidacticiel',
        'TIMEOUT': 300,
    }
}

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
# ⭐ MISE À JOUR : 'Lax' comme valeur de base sécurisée et fonctionnelle en HTTP (sera écrasée en production)
SESSION_COOKIE_SAMESITE = 'Lax' 
SESSION_COOKIE_SECURE = False 
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# =========================================================================
# 5. AUTHENTIFICATION DJANGO
# =========================================================================

# Logique : Permet la connexion par ModelBackend (mot de passe) et AuthenticationBackend (allauth).
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  
)
ANONYMOUS_USER_NAME = None

# Password validation 
AUTH_PASSWORD_VALIDATORS = [
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
# 6. INTERNATIONALISATION & FICHIERS
# =========================================================================

# Internationalization 
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = "Africa/Porto-Novo"
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================================================
# 7. CONFIGURATION REST FRAMEWORK & JWT
# =========================================================================

# Site framework (requis par allauth)
SITE_ID = 1

# Configuration dj-rest-auth.
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'SESSION_LOGIN': False,
    'USER_DETAILS_SERIALIZER': 'apps.users.serializers.UserSerializer',
    'JWT_AUTH_COOKIE': 'cv_didacticiel_jwt',
    'JWT_AUTH_REFRESH_COOKIE': 'cv_didacticiel_jwt_refresh',
    
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
    'REGISTER_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}

# Configuration allauth pour la gestion de l'email/mot de passe.
ACCOUNT_EMAIL_VERIFICATION = 'none' 
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_METHODS = {'email'}  
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*'] 
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = False 

# Django REST Framework 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
        'rest_framework.authentication.SessionAuthentication',
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
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SIMPLE JWT configuration
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

# Cookies JWT HttpOnly
JWT_COOKIE_NAME = "cv_didacticiel_jwt"
JWT_REFRESH_COOKIE_NAME = "cv_didacticiel_jwt_refresh"
JWT_COOKIE_SECURE = env.bool('JWT_COOKIE_SECURE', default=False) 
JWT_COOKIE_SAMESITE = "Lax"    
JWT_COOKIE_HTTPONLY = True

# CORS settings
# SÛR PAR DÉFAUT : Sera écrasé par development.py
CORS_ALLOW_ALL_ORIGINS = False 

# Origines autorisées par défaut (surtout si DEBUG=False)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    FRONTEND_URL 
])

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# MODIFIE POUR CV DIDACTICIEL: Documentation API 
SPECTACULAR_SETTINGS = {
    'TITLE': 'CV Didacticiel Platform API',
    'DESCRIPTION': 'API complète pour la plateforme de mise de création de cv en ligne, proffessionel, compatible et recommander.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'TAGS': [
        {'name': 'Authentication', 'description': 'Endpoints d\'authentification'},
        {'name': 'users', 'description': 'Gestion des comptes utilisateurs'},
        {'name': 'cv_app', 'description': 'Création, gestion et téléchargement de CV'},
       
    ],
}

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

# Email configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@cvdidacticiel.bj')

# Logging 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # (handlers et loggers)
}

# Celery Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Configuration des thumbnails 
THUMBNAIL_ALIASES = {
    '': {
        'profile_pic_small': {'size': (50, 50), 'crop': True},
        'profile_pic_medium': {'size': (150, 150), 'crop': True},
        'work_photo_thumb': {'size': (200, 150), 'crop': True},
        'work_photo_large': {'size': (800, 600), 'crop': False},
    },
}

# Security settings 
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
# HSTS est désactivé si DEBUG=True
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# MODIFIE POUR CV DIDACTICIEL: Settings spécifiques à l'application 
APP_SETTINGS = {
    'MAX_CV_DESCRIPTION_LENGTH': 5000,
    'MAX_CV_PER_USER': 10,
    'ALLOWED_IMAGE_TYPES': ['jpg', 'jpeg', 'png'],
    'MAX_UPLOAD_SIZE': 5 * 1024 * 1024, 
    'PRICE_CV_DOWNLOAD': env.int('PRICE_CV_DOWNLOAD', default=2500) 
}

# MODIFIE POUR CV DIDACTICIEL: Rate limiting spécifique 
API_RATE_LIMITS = {
    'cv_creation': '5/hour',
    'user_registration': '3/hour',
    'password_reset': '5/hour',
    'profile_update': '20/hour',
}

# MODIFIE POUR CV DIDACTICIEL: Feature flags 
FEATURE_FLAGS = {
    'GENERATION_AI': env.bool('FEATURE_GENERATION_AI', default=True),
}

# File storage (pour production avec AWS S3) 
if env.bool('USE_S3', default=False):
    # ... (configuration S3)
    pass