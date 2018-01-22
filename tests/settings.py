# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django


DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "y0e$ul(qbzsk0!*gl*_qfjf6*3+58x^syqutruutvnxh^-rw_5"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_undeletable",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

EMAIL_OVERRIDE_ADDRESS = 'do-not-reply@example.com'
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# disable migrations
MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,

    'django_undeletable': None,
}
