"""
Django settings for delft3d project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import djcelery
djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

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

    'djcelery',

    'delft3dworker',
    'delft3dgtfrontend',
]

MIDDLEWARE_CLASSES = [
   'django.middleware.security.SecurityMiddleware',
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'delft3dgtmain.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '/opt/delft3d-gt/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ['/opt/delft3d-gt/delft3d-gt-ui/dist', ]

TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [STATIC_ROOT, ],
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

WSGI_APPLICATION = 'delft3dgtmain.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Login
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Celery

BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Amsterdam'
CELERY_ENABLE_UTC = True

WORKER_FILEURL = '/files'

# import provisioned settings
try:
    from provisionedsettings import *
except ImportError:
    SECRET_KEY = 'test'

################## TESTING

if 'test' in sys.argv:

    from teamcity import is_running_under_teamcity

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

    # BROKER_BACKEND='memory'
    CELERY_RESULT_BACKEND = 'cache'
    CELERY_CACHE_BACKEND = 'memory'

    COVERAGE_REPORT_HTML_OUTPUT_DIR = 'test/coverage'
    COVERAGE_PATH_EXCLUDES = [
        r'.*migrations.*'
    ]
    COVERAGE_MODULE_EXCLUDES = [
        '__init__',
        'common.views.test',
        'django',
        'djcelery',
        'locale$',
        'migrations'
        'settings$',
        'tests$',
        'urls$',
    ]

    DELFT3DGTRUNNER = 'delft3dworker.tests.Delft3DGTRunner'
    TEAMCITYDELFT3DGTRUNNER = 'delft3dworker.tests.TeamcityDelft3DGTRunner'
    TEST_RUNNER = TEAMCITYDELFT3DGTRUNNER if is_running_under_teamcity() else DELFT3DGTRUNNER

