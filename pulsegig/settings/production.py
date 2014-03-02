from .base import *
import os

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DEBUG = False

ALLOWED_HOSTS = ['pulsegig.com', 'www.pulsegig.com', 'manage.pulsegig.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['PULSEGIG_DB_NAME'],
        'USER': os.environ['PULSEGIG_DB_USER'],
        'PASSWORD': os.environ['PULSEGIG_DB_PASSWORD'],
        'HOST': '',
        'PORT': '',
    }
}
