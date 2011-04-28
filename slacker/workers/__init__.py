from slacker.workers.local import DummyWorker, ThreadWorker
from slacker.workers.http import HttpWorker, CurlHttpWorker

try:
    from slacker.workers.django import DjangoWorker
except ImportError: # django is not installed
    pass
