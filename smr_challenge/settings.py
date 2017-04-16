"""
Django settings for smr_challenge project.

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ntegwv=1ps%m@14g9mfga%-dq@!9(z0a^4)3u5l+1$o^yk0(8u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'treebeard',
    'messageboard',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
# Normally I wouldn't ever consider disabling CSRF middleware, but
# conveying the CSRF token to the front is a problem I'm not going
# to address right now.
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smr_challenge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smr_challenge.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# +---------------------------------------------------------------------------+
# |                                                                           |
# |                        django.contrib.staticfiles                         |
# |                                                                           |
# +---------------------------------------------------------------------------+

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# +---------------------------------------------------------------------------+
# |                                                                           |
# |                                channels                                   |
# |                                                                           |
# +---------------------------------------------------------------------------+

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgiref.inmemory.ChannelLayer',
        'ROUTING': 'messageboard.routing.routing'
    }
}

# +---------------------------------------------------------------------------+
# |                                                                           |
# |                          django-cors-headers                              |
# |                                                                           |
# +---------------------------------------------------------------------------+

from corsheaders.defaults import default_headers

# Cross-origin requests are necessary while developing.
CORS_ORIGIN_WHITELIST = [
    'localhost:3000'
]

CORS_ALLOW_CREDENTIALS = True

# +---------------------------------------------------------------------------+
# |                                                                           |
# |                              messageboard                                 |
# |                                                                           |
# +---------------------------------------------------------------------------+

ROOT_CHANNEL_NAME = 'home'
ROOT_CHANNEL_LIMIT = 10

# +---------------------------------------------------------------------------+
# |                                                                           |
# |                              local_settings.py                            |
# |                      Don't add settings below this line.                  |
# +---------------------------------------------------------------------------+

from local_settings import *