from functools import partial
from tornado import stack_context
from tornado.ioloop import IOLoop
from slacker.postpone import safe_proceed

class DummyWorker(object):
    """ Dummy worker for local immediate execution """
    def proceed(self, postponed, callback = None):
        # safe_proceed is called instead of _proceed
        # for consistent error handling
        res = safe_proceed(postponed)
        if callback:
            callback(res)


class ThreadWorker(object):
    """
    Executes code in a thread from a ThreadPool.

    .. warning::

        postponed code shouldn't interact with tornado because
        tornado is not thread-safe.

    .. waring::

        I'm bad at threads so this can be broken ;)
    """

    _default_pool = None

    def __init__(self, pool=None, ioloop=None):
        """
        Initializes ThreadWorker.
        'pool' is a multiprocessing.pool.ThreadPool instance,
        'ioloop' is a tornado.ioloop.IOLoop instance.
        """
        self.ioloop = ioloop or IOLoop.instance()

         # create default pool only if necessary
        if not pool and not self.__class__._default_pool:
            from multiprocessing.pool import ThreadPool
            self.__class__._default_pool = ThreadPool(5)

        self.pool = pool or self.__class__._default_pool


    def proceed(self, postponed, callback=None):
        _proceed = partial(safe_proceed, postponed)

        if callback is None:
            self.pool.apply_async(_proceed)
            return

        # Without stack_context.wrap exceptions will not be propagated,
        # they'll be catched by tornado. Hours of debugging ;)
        @stack_context.wrap
        def on_response(result):
            self.ioloop.add_callback(partial(callback, result))

        self.pool.apply_async(_proceed, callback = on_response)
