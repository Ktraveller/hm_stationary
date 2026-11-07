import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔐 SECURITY
# =========================

SECRET_KEY = 'django-insecure-local-key'

DEBUG = True

ALLOWED_HOSTS = ['*']


# =========================
# 📦 APPS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',

    'stationary_system',
]


# =========================
# 🌐 MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'hm_stationary.urls'


# =========================
# 📄 TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # you can add templates folder later
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


WSGI_APPLICATION = 'hm_stationary.wsgi.application'
ASGI_APPLICATION = 'hm_stationary.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


# =========================
# 🗄️ DATABASE
# =========================

DATABASE_URL = os.environ.get('DATABASE_URL')
IS_RENDER = os.environ.get('RENDER') == 'true' or bool(os.environ.get('RENDER_SERVICE_ID'))

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
elif IS_RENDER:
    raise ImproperlyConfigured(
        'DATABASE_URL is required on Render. Set it to the PostgreSQL database URL.'
    )
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =========================
# 🔑 AUTH
# =========================

AUTH_USER_MODEL = 'stationary_system.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================
# 🌍 INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Dar_es_Salaam'
USE_I18N = True
USE_TZ = True


# =========================
# 📦 STATIC FILES
# =========================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# =========================
# 📁 MEDIA FILES
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# 🔐 SECURITY (SIMPLIFIED)
# =========================

CSRF_TRUSTED_ORIGINS = []

X_FRAME_OPTIONS = 'SAMEORIGIN'

CORS_ALLOW_ALL_ORIGINS = True  # OK for local only