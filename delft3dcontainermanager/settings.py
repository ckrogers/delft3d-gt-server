"""
Django settings for delft3d project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'delft3dcontainermanager',
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ######
# Celery
# ######

BROKER_URL = 'redis://172.31.42.27'
CELERY_RESULT_BACKEND = 'redis://172.31.42.27'

# Disabling rate limits altogether is recommended if you don't have any tasks
# using them. This is because the rate limit subsystem introduces quite a lot
# of complexity.
CELERY_DISABLE_RATE_LIMITS = True

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TRACK_STARTED = True  # All pending tasks can be revoked
CELERY_TASK_PUBLISH_RETRY = False  # No retry on connection error
CELERY_MESSAGE_COMPRESSION = 'gzip'  # Can help on docker inspect messages

# Custom task expire time
TASK_EXPIRE_TIME = 5 * 60  # After 5 minutes, tasks are forgotten
CELERY_TASK_RESULT_EXPIRES = 5 * 60  # After 5 minutes redis keys are deleted

# Worker specific settings, becomes important
# with cloud workers, when there are multiple
# workers for each queue.
CELERY_ACKS_LATE = False
CELERYD_PREFETCH_MULTIPLIER = 1

# import provisioned settings
try:
    from delft3dgtmain.provisionedsettings import *
except ImportError:
    SECRET_KEY = 'test'
