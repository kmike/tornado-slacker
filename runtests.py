#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from django.conf import settings
from django.core.management import call_command

# always use async_orm from the checkout, not the installed version
sys.path.insert(0, os.path.dirname(__file__))

settings.configure(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',

        'async_orm',
    ),
    DATABASES = {
        'default': dict(
            ENGINE = 'django.db.backends.sqlite3',
        )
    }
)

if __name__ == "__main__":
    call_command('test', 'async_orm')
