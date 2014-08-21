==================
Django Undeletable
==================

Django Undeletable provides a base model with useful default attributes to keep track of your data.
But the actual reason, I created this package, is to have the ability to delete data without wiping it from the database. This is achived through a secondary manager called data, that has an overwitten delete method and a filtered default queryset, which only lets you see undeleted datasets.

Installation
============

pip install django-undeletable

When using this package, all your models should extend this packages BaseModel instead of django.db.models.Model.


Benefits
--------

While deriving from the BaseModel you get the following:

* Your models have a created, modified and deleted DateTime attribute
* Your models have an active flag, marking it as deleted if FALSE
* Your models have the normal objects queryset to stay compatible to the Django Admin
* Your models have a data queryset which acts as the default for any app that uses model._default_manager instead of model.objects

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.
