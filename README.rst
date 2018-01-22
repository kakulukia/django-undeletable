=============================
django-undeletable
=============================

.. image:: https://badge.fury.io/py/django-undeletable.svg
    :target: https://badge.fury.io/py/django-undeletable

.. image:: https://travis-ci.org/kakulukia/django-undeletable.svg?branch=master
    :target: https://travis-ci.org/kakulukia/django-undeletable

.. image:: https://codecov.io/gh/kakulukia/django-undeletable/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kakulukia/django-undeletable

undeletable Django models

Documentation
-------------

The full documentation is at https://django-undeletable.readthedocs.io.

Quickstart
----------

Install django-undeletable::

    pip install django-undeletable

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_undeletable.apps.DjangoUndeletableConfig',
        ...
    )

Add django-undeletable's URL patterns:

.. code-block:: python

    from django_undeletable import urls as django_undeletable_urls


    urlpatterns = [
        ...
        url(r'^', include(django_undeletable_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
