#!/usr/bin/env python
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'redis_admin',
        ),
        ROOT_URLCONF=None,
        SECRET_KEY='foobar',
        CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': '%s:%s' % ('127.0.0.1', 6379),
                'OPTIONS': {
                    'DB': 0,
                    'PASSWORD': '',
                    'MIN_COMPRESSION_LEN': 102400,
                },
            }
        }
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:] + ['redis_admin']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()