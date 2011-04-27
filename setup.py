#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop', 'upload_sphinx', 'build_sphinx'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version='0.0.1'

setup(
    name = 'django-async-orm',
    version = version,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'https://github.com/kmike/django-async-orm/',
    download_url = 'https://bitbucket.org/kmike/django-async-orm/get/tip.zip',

    description = 'This app makes non-blocking django ORM calls possible (currently using tornado.httpclient.AsyncHTTPClient)',
    long_description = open('README.rst').read(),
    license = 'MIT license',
    requires = ['django (>=1.2)', 'tornado (>= 1.2)'],

    packages=[
        'async_orm',
        'async_orm.vendor',
        'async_orm.incarnations',
        'async_orm.incarnations.http'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Tornado',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
        'Topic :: Database',
    ],
)
