import os
from datetime import timedelta
from pathlib import Path

from config.config import settings as settings

# from dotenv import load_dotenv
# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.DEBUG

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = settings.INSTALLED_APPS

MIDDLEWARE = settings.MIDDLEWARE

ROOT_URLCONF = settings.ROOT_URLCONF

TEMPLATES = settings.TEMPLATES

WSGI_APPLICATION = settings.WSGI_APPLICATION


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = settings.DATABASES

if DEBUG:
    name = DATABASES['default']['NAME']
    DATABASES['default']['NAME'] = os.path.join(BASE_DIR, name)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = settings.AUTH_PASSWORD_VALIDATORS

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = settings.LANGUAGE_CODE
TIME_ZONE = settings.TIME_ZONE
USE_I18N = settings.USE_I18N
USE_TZ = settings.USE_TZ

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = settings.STATIC_URL
MEDIA_URL = settings.MEDIA_URL

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = settings.DEFAULT_AUTO_FIELD

# doct24
AUTH_USER_MODEL = settings.AUTH_USER_MODEL
CORS_ORIGIN_ALLOW_ALL = settings.CORS_ORIGIN_ALLOW_ALL  # processing requests from all domains
CORS_ALLOW_CREDENTIALS = settings.CORS_ALLOW_CREDENTIALS
ASGI_APPLICATION = settings.ASGI_APPLICATION

REST_FRAMEWORK = settings.REST_FRAMEWORK

SECURE_PROXY_SSL_HEADER = settings.SECURE_PROXY_SSL_HEADER

SWAGGER_SETTINGS = settings.SWAGGER_SETTINGS

'''Блок для перезапись параметров проекта из ENVIRON. ОБЯЗАТЕЛЬНО ЭТОТ БЛОК 
В КОНЦЕ ЭТОГО МОДУЛЯ'''
if settings.ENVIRON:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = int(os.environ.get("DEBUG", default=0))
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE",
                                     "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'uid'
}

# Отображение пустого поля в админке
EMPTY_FIELD = '-пусто-'


CORS_ALLOWED_ORIGINS = ['http://localhost:8000']
CORS_ALLOW_CREDENTIALS = True
# CORS_REPLACE_HTTPS_REFERER = True
#
# CSRF_TRUSTED_ORIGINS = [
#     'localhost:8000',
#     'localhost'
# ]
