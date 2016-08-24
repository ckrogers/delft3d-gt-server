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

    'rest_framework',
    'crispy_forms',
    'guardian',
    'delft3dcontainermanager',
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

# Object permissions

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
]

ANONYMOUS_USER_NAME = None  # No anon user

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '/opt/delft3d-gt/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ['/opt/delft3d-gt/delft3d-gt-ui/dist/']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [STATIC_ROOT],
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
        'NAME': 'django.contrib.auth.password_validation'
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.NumericPasswordValidator',
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

# ######
# Celery
# ######

BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'

# Disabling rate limits altogether is recommended if you don't have any tasks
# using them. This is because the rate limit subsystem introduces quite a lot
# of complexity.
CELERY_DISABLE_RATE_LIMITS = True

# If True the task will report its status as started when the task is
# executed by a worker.
CELERY_TRACK_STARTED = True

# Time (in seconds, or a timedelta object) for when after stored task
# tombstones will be deleted. A built-in periodic task will delete the results
# after this time (celery.task.backend_cleanup). A value of None or 0 means
# results will never expire (depending on backend specifications). Default is
# to expire after 1 day. This resulted in losing task status.
CELERY_TASK_RESULT_EXPIRES = None

# Timeout before task is retried. So when a task is queued but not executed
# for half a day (standard) the task is send again. This explains
# many identical tasks running, in turn keeping many other tasks pending.
# Timeout should be set to (at least) twice the maximum runtime of task
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 5184000}  # 60 days

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Amsterdam'
CELERY_ENABLE_UTC = True

# Worker specific settings, becomes important
# with cloud workers, when there are multiple
# workers for each queue.
CELERY_ACKS_LATE = False
CELERYD_PREFETCH_MULTIPLIER = 1

WORKER_FILEURL = '/files'

# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'delft3dworker.authentication.CsrfExemptSessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
        # 'delft3dworker.permissions.ViewObjectPermissions',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        # 'rest_framework.filters.DjangoObjectPermissionsFilter',
    ]
}


# import provisioned settings
try:
    from provisionedsettings import *
except ImportError:
    SECRET_KEY = 'test'

# TESTING

if 'test' in sys.argv:

    from teamcity import is_running_under_teamcity

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Debug on running tests
    DEBUG = True

    # BROKER_BACKEND='memory'
    CELERY_RESULT_BACKEND = 'cache'
    CELERY_CACHE_BACKEND = 'memory'

    WORKER_FILEDIR = 'test/'

    DELFT3DGTRUNNER = 'delft3dworker.tests.Delft3DGTRunner'
    TEAMCITYDELFT3DGTRUNNER = 'delft3dworker.tests.TeamcityDelft3DGTRunner'
    TEST_RUNNER = TEAMCITYDELFT3DGTRUNNER if is_running_under_teamcity(
    ) else DELFT3DGTRUNNER

    CELERY_ALWAYS_EAGER = True

    DELFT3D_DUMMY_IMAGE_NAME = 'dummy_simulation'
    POSTPROCESS_DUMMY_IMAGE_NAME = 'dummy_postprocessing'
    PREPROCESS_DUMMY_IMAGE_NAME = 'dummy_preprocessing'
    PROCESS_DUMMY_IMAGE_NAME = 'dummy_processing'
    EXPORT_DUMMY_IMAGE_NAME = 'dummy_export'

    DELFT3D_IMAGE_NAME = 'dummy_simulation'
    POSTPROCESS_IMAGE_NAME = 'dummy_postprocessing'
    PREPROCESS_IMAGE_NAME = 'dummy_preprocessing'
    PROCESS_IMAGE_NAME = 'dummy_processing'
    EXPORT_IMAGE_NAME = 'dummy_export'
