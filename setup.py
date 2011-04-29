#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop', 'upload_sphinx', 'build_sphinx'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version='0.0.2'

setup(
    name = 'tornado-slacker',
    version = version,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'https://github.com/kmike/tornado-slacker/',
    download_url = 'https://bitbucket.org/kmike/tornado-slacker/get/tip.zip',

    description = 'This package provides an easy API for moving the work out of the tornado process / event loop.',
    long_description = open('README.rst').read(),
    license = 'MIT license',
    requires = ['tornado (>= 1.2)'],

    packages=[
        'slacker',
        'slacker.workers',
        'slacker.django_backend',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
    ],
)
