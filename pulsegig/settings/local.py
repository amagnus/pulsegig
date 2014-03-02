from .base import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEV_PUBLIC_IP = os.environ['DEV_PUBLIC_IP']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_DEV_NAME'],
        'USER': os.environ['DB_DEV_USER'],
        'PASSWORD': os.environ['DB_DEV_PASSWORD'],
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []
