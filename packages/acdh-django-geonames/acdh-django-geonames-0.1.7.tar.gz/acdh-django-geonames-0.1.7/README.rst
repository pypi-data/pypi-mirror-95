=============================
GeoName Places
=============================

.. image:: https://badge.fury.io/py/acdh-django-geonames.svg
    :target: https://badge.fury.io/py/acdh-django-geonames

.. image:: https://travis-ci.com/acdh-oeaw/acdh-django-geonames.svg?branch=master
    :target: https://travis-ci.com/acdh-oeaw/acdh-django-geonames

.. image:: https://readthedocs.org/projects/geonames-utils/badge/?version=latest
    :target: https://geonames-utils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/acdh-oeaw/acdh-django-geonames/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/acdh-oeaw/acdh-django-geonames

A django package providing models and views for Geoname Places

Documentation
-------------

The full documentation is at https://acdh-django-geonames.readthedocs.io.

Quickstart
----------

Install GeoName Places::

    pip install acdh-django-geonames

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'gn_places.apps.GnPlacesConfig',
        ...
    )

Add GeoName Places's URL patterns:

.. code-block:: python

    from gn_places import urls as gn_places_urls


    urlpatterns = [
        ...
        url(r'^', include(gn_places_urls)),
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


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
