django-epfl-misc
================

[![Build Status][github-actions-image]][github-actions-url]
[![Coverage Status][codecov-image]][codecov-url]
[![PyPI version][pypi-image]][pypi-url]
[![PyPI Python version][pypi-python-image]][pypi-url]

A Django application with helper functions and utilities.

Requirements
------------

- Python 2.7, 3.5 or later
- Django 1.11, 2.2

Installation
------------

Installing from PyPI is as easy as doing:

```bash
pip install django-epfl-misc
```

Documentation
-------------

### Auth

#### `superuser_required_or_403()`

```python
from django_epflmisc.decorators import superuser_required_or_403

@superuser_required_or_403()
def my_view(request):
    # I can assume now that the view is only accessible as a superuser.
```

### Cache

The cache system requires a small amount of setup. Namely, you have to tell
it where your cached data should live – whether in a database, on the
filesystem or directly in memory.

See [Django's cache framework][django-cache]

#### `cache_anonymous_user(timeout, cache="default")`

```python
from django_epflmisc.decorators import cache_anonymous_user

@cache_anonymous_user(60 * 15)
def my_view(request):
    # I can assume now that the view is cached for anonymous users.
```

License
-------

The MIT License (MIT)

Copyright (c) 2021 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI.

[github-actions-image]: https://github.com/epfl-si/django-epfl-misc/workflows/Build/badge.svg?branch=main
[github-actions-url]: https://github.com/epfl-si/django-epfl-misc/actions

[codecov-image]:https://codecov.io/gh/epfl-si/django-epfl-misc/branch/main/graph/badge.svg
[codecov-url]:https://codecov.io/gh/epfl-si/django-epfl-misc

[pypi-python-image]: https://img.shields.io/pypi/pyversions/django-epfl-misc
[pypi-image]: https://img.shields.io/pypi/v/django-epfl-misc
[pypi-url]: https://pypi.org/project/django-epfl-misc/

[django-cache]: https://docs.djangoproject.com/en/2.2/topics/cache/#setting-up-the-cache
