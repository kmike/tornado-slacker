#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from django.core.management import execute_manager

# always use slacker from the checkout, not the installed version
sys.path.insert(0, os.path.dirname(__file__))

# add project to pythonpath
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test_project'))

sys.argv.insert(1, 'test')
if len(sys.argv) == 2:
    sys.argv.extend(['testapp'])

from test_project import settings
execute_manager(settings)
