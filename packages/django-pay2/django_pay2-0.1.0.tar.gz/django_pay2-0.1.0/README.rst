=============================
Django Pay
=============================

.. image:: https://travis-ci.org/la1t/django_pay2.svg?branch=master
    :target: https://travis-ci.org/la1t/django_pay2

Easy payments systems integration for Django

Quickstart
----------

Install Django Pay::

    pip install django_pay2

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pay2',
        ...
    )

Add Django Pay's URL patterns:

.. code-block:: python


    urlpatterns = [
        ...
        url(r'^', include('django_pay2.urls')),
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
