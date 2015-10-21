
# Django Undeletable

Django Undeletable provides a base model with useful default attributes to keep track of your data.
But the actual reason, I created this package, is to have the ability to delete data without wiping it from the database.
This is achived through a custom manager called data, that has a custom delete method and a filtered default queryset, which only lets you see undeleted datasets.

### Installation

    pip install django-undeletable

When using this package, all your models should extend this packages BaseModel instead of django.db.models.Model.


### Benefits

While deriving from the BaseModel you get the following:

* Your models have a created, modified and deleted DateTime attribute
* Your models have NO objects queryset to kinda show of that they behave differently and because im kinda lazy about writing - its still compatible because
Django actually uses the _default_manager and does not care about its name (a sloppy written 3rd party app might, tho)
