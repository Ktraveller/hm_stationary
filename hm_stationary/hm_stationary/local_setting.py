import os
from pathlib import Path

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

    'stationary_system',
]


# =========================
# 🌐 MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Remove whitenoise for local dev (optional)
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


# =========================
# 🗄️ DATABASE (SQLITE LOCAL)
# =========================

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

# For local dev, this is enough
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


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