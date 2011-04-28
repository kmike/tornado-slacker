from __future__ import absolute_import

from django.core.urlresolvers import reverse
from slacker.django_backend.conf import SLACKER_SERVER
from slacker.workers.http import HttpWorker

class DjangoWorker(HttpWorker):

    """ HttpWorker with django's defaults """

    def __init__(self, server=None, path=None):
        server = server or SLACKER_SERVER
        path = path or reverse('slacker-execute')
        super(DjangoWorker, self).__init__(server, path)

