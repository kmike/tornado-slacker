try:
    import cPickle as pickle
except ImportError:
    import pickle

from tornado.httpclient import AsyncHTTPClient

class TornadoAsyncHttpWorker(object):
    """
    This worker sends pickled postponed object to a web server via
    HTTP POST request and waits for a response. Response is unpickled
    and passed to the callback.

    Combined with traditional threaded web server like apache2 + mod_wsgi
    this enables easy deployment and thread pool for free (managed by
    webserver). HTTP, however, may cause a significant overhead.

    Django backend implementation can be found at ``slacker.django_backend``.
    """

    def __init__(self, server='127.0.0.1:8000', path='/'):
        self.url = server + path

    def proceed(self, postponed, callback):

        def on_response(response):
            result = pickle.loads(response.body)
            callback(result)

        http = AsyncHTTPClient()
        http.fetch(self.url, on_response, method='POST', body=postponed._pickled)
