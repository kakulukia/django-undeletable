django-undeletable |BuildStatus|_ |Coverage|_
==============================================================

.. |BuildStatus| image:: https://travis-ci.org/kakulukia/django-undeletable.svg
.. _BuildStatus: https://travis-ci.org/kakulukia/django-undeletable

.. |Coverage| image:: https://codecov.io/gh/kakulukia/django-undeletable/branch/master/graph/badge.svg
.. _Coverage: https://codecov.io/gh/kakulukia/django-undeletable


I have run into dozens of situations where data got deleted by accident or somebody
wanted to know when something got deleted or changed, so this little module will prevent
accidents and you will always be able to reverse the situation or to identify why that
little bug deleted exactly this set of data.
And even if somebody from marketing all in a sudden wants to know what was in those
temporary shopping baskets that should have been deleted already - you will be able to answer
those questions! I never had the problem of too much data - it was always the missing data,
the missing creation and modification timestamps that makes your job harder than it has to be.

So here is the answer to all that. Nothing will be deleted anymore and you will know when X
got created, changed or deleted. Django Undeletable provides a **BaseModel** with useful
default attributes to keep track of your data. The custom **DataManager** keeps track of
deleted and live data. You can also keep stuff hidden from the public while displaying
that data to some chosen customers (like beta testers).


Installation
--------------

Install django-undeletable

.. code-block:: bash

    pip install django-undeletable

When using this package, all your models should extend from BaseModel
instead of django.db.models.Model. Take a look at the additional NamedModel as to how its
done.

.. code-block:: python

    class NamedModel(BaseModel):
        name = models.CharField(_('Name'), max_length=150, db_index=True)

        class Meta(BaseModel.Meta):
            ordering = ['name']
            abstract = True

Extending the *Meta* class from *BaseModel.Meta* is important for Django 2.0+ otherwise you will experience
your related QuerySets to not be managed by a DataManager but by Djangos default manager instead including
deleted data.

For a fully working QuerySet and Manager relation which share methods, you should create your managers the following way:

.. code-block:: python

    class BookQuerySet(DataQuerySet):
        def not_null(self):
            return self.filter(author__isnull=False)


    class CoverBook(Book):
        data = DataManager.from_queryset(BookQuerySet)()

This way you can do `CoverBook.data.all().nut_null()` and `CoverBook.data.nut_null()` otherwise you will have
to define the methods twice or face errors in one of the previous calls.

Features
----------

While inheriting from BaseModel you get the following advantages:

* Your models have created, modified and deleted DateTime attributes
* The *data* queryset shall always tell you which ones of your models are undeletable
  or from 3rd party modules - but the main reason for using data is that im lazy and
  prefer typing data instead of objects :)
* Since quite some modules don't respect a models default manager and just use 'objects',
  data is mirrored to objects to not run into any trouble
* You have the option to hide specific data from the public while using *visible()* instead of *all()*
* since its quite common, this package also includes the above NamedModel and a customized
  User Model that you should copy to your codebase and remove the *abstract = True* line to have undeletable users
* The included abstract User class features an EMAIL_OVERRIDE_ADDRESS setting that can be
  used to not actually email real users on a development system :)


Running Tests
---------------

Does the code actually work?

.. code-block:: bash

    make init
    make test

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
