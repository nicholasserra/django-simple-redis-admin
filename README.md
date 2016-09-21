[![Build Status](https://travis-ci.org/nicholasserra/django-simple-redis-admin.svg?branch=travis)](https://travis-ci.org/nicholasserra/django-simple-redis-admin)

django-simple-redis-admin
=========

`django-simple-redis-admin` is an addition to your Django admin panel that allows you to view and delete your Redis keys.

Requirements
------------
* Django >= 1.8 <= 1.10
* A Django redis cache backend. I recommend [django-redis-cache](https://github.com/sebleier/django-redis-cache)

Installation
------------
`django-simple-redis-admin` can be installed via pip.

```
pip install django-simple-redis-admin
```

Then just add `redis_admin` to your `INSTALLED_APPS`.

Why simple?
-----------

This package does not use models, so no database tables need to be created. Just add to INSTALLED_APPS and go.
Users must have is_superuser == True to view the Redis admin. No django admin logs are created with this package.

To Do
-----
* Editing keys
* Better representation for Redis sets
