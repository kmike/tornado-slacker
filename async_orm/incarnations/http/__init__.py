# coding: utf8
"""

This async_orm incarnation makes django ORM queries async
by executing them in django view and fetching the results via
http using tornado's async http client.

This way we get a simple implementation, easy deployment and a
thread pool (managed by webserver) for free.

Http, however, can cause a significant overhead.

"""

try:
    import cPickle as pickle
except ImportError:
    import pickle

from tornado.httpclient import AsyncHTTPClient
from django.core.urlresolvers import reverse

from async_orm.vendor import adisp
from async_orm.chains import ModelChainProxy, ProxyWrapper
from async_orm.settings import HTTP_SERVER


class TornadoHttpModelProxy(ModelChainProxy):

    def execute(self, callback):
        server = self._extra.get('server', HTTP_SERVER)
        path = self._extra.get('path', None) or reverse('async-orm-execute')
        url = server + path

        def on_response(response):
            result = pickle.loads(response.body)
            callback(result)

        http = AsyncHTTPClient()
        http.fetch(url, on_response, method='POST', body=self._pickled)

    fetch = adisp.async(execute)



class AsyncWrapper(ProxyWrapper):
    """
    Returns async proxy for passed django.db.models.Model class.
    Constructor also accepts 'server' and 'path' keyword arguments.

    'async-orm-execute' view enabled.

    Example::

        from django.contrib.auth.models import User
        from async_orm.incarnations.http import AsyncWrapper

        AsyncUser = AsyncWrapper(User, server='http://127.0.0.1:8001')

    """
    proxy_class = TornadoHttpModelProxy
