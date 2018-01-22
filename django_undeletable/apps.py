# -*- coding: utf-8
from django.apps import AppConfig


class DjangoUndeletableConfig(AppConfig):
    name = 'django_undeletable'
    verbose_name = "Django undeletable models"

    def ready(self):
        pass
