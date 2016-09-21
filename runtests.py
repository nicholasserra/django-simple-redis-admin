#!/usr/bin/env python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    TEMPLATE_DEBUG = True
    TEMPLATE_DIRS = [
        os.path.join(os.path.dirname(__file__), 'redis_admin', 'templates'),
    ]
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
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware'
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
        },
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': TEMPLATE_DIRS,
                'APP_DIRS': True,
                'OPTIONS': {
                    'debug': TEMPLATE_DEBUG,
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        TEMPLATE_DIRS=TEMPLATE_DIRS,
        TEMPLATE_DEBUG=TEMPLATE_DEBUG
    )


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:] + ['redis_admin']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
