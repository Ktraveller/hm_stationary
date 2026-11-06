import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔐 SECURITY
# =========================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-key'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]


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

    'stationary_system',
]


# =========================
# 🌐 MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise for static files
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
        'DIRS': [],
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


# =========================
# 🗄️ DATABASE
# =========================

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# =========================
# 🔑 AUTH
# =========================

AUTH_USER_MODEL = 'stationary_system.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
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

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# =========================
# 📁 MEDIA FILES
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# 🔐 SECURITY SETTINGS
# =========================

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

CORS_ALLOW_ALL_ORIGINS = True


# =========================
# 🔒 HTTPS SETTINGS
# =========================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG