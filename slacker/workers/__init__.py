from __future__ import absolute_import
from .local import DummyWorker, ThreadWorker
from .http import HttpWorker, CurlHttpWorker

try:
    from .django import DjangoWorker
except ImportError, e: # django is not installed
    import warnings
    warnings.warn("DjangoWorker is not available: %s" % e)
