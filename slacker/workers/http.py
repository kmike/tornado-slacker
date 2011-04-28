try:
    import cPickle as pickle
except ImportError:
    import pickle

from tornado.httpclient import AsyncHTTPClient
from tornado.curl_httpclient import CurlAsyncHTTPClient


class HttpWorker(object):
    """
    This worker sends pickled postponed object to a web server via
    HTTP POST request and waits for a response. Response is unpickled
    and passed to the callback.

    Combined with traditional threaded web server like apache2 + mod_wsgi
    or cherrypy this enables easy deployment, code islation and a thread
    pool for free (managed by webserver). HTTP and pickling/unpickling
    the result, however, may cause a significant overhead.

    Django backend implementation can be found at ``slacker.django_backend``.
    """

    HTTPClient = AsyncHTTPClient

    def __init__(self, server='127.0.0.1:8000', path='/'):
        self.url = server + path

    def proceed(self, postponed, callback):

        def on_response(response):
            result = pickle.loads(response.body)
            callback(result)

        http = self.HTTPClient()
        http.fetch(self.url, on_response, method='POST', body=postponed._pickled)


class CurlHttpWorker(HttpWorker):
    """ HttpWorker that uses CurlAsyncHTTPClient instead of AsyncHTTPClient """
    HTTPClient = CurlAsyncHTTPClient

