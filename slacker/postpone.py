import pprint
import sys
import types

try:
    import cPickle as pickle
except ImportError:
    import pickle

from slacker.workers.local import DummyWorker

class SlackerException(Exception):
    pass

class _Module(object):
    """ Helper class for pickling python modules """

    def __init__(self, module):
        self.module = module

    def __getstate__(self):
        return self.module.__name__

    def __setstate__(self, name):
        __import__(name)
        self.module = sys.modules[name]


class Postponed(object):
    """
    Stores attribute, call and slice chain without actully
    calling methods, accessing attributes and performing slicing.

    Wrapped object and method arguments must be picklable.

    Collecting the access to private methods and attributes
    (beginning with __two_underscores) is not supported.

    FIXME: some attributes (e.g. '_obj', '_chain', '_extra', 'proceed')
    of original object are replaced with the ones from this proxy.
    """

    def __init__(self, obj, worker = None):
        self._obj = obj
        self._chain = []
        self._worker = worker or DummyWorker()

    def __repr__(self):
        return "%s: %s" % (self._obj, pprint.pformat(self._chain))

    def __getstate__(self):

        if isinstance(self._obj, types.ModuleType):
            return self._chain, _Module(self._obj)

        return self._chain, self._obj

    def __setstate__(self, state):
        self._chain, self._obj = state

        if isinstance(self._obj, _Module):
            self._obj = self._obj.module

        # always use local worker after unpickling
        self._worker = DummyWorker()

    @property
    def _pickled(self):
        return pickle.dumps(self, pickle.HIGHEST_PROTOCOL)

    def __getattr__(self, attr):
        # pickle.dumps internally checks if __getnewargs__ is defined
        # and thus returning ChainProxy object instead of
        # raising AttributeError breaks pickling. Returning self instead
        # of raising an exception for private attributes can possibly
        # break something else so the access to other private methods
        # and attributes is also not overriden.
        if attr.startswith('__'):
            return self.__getattribute__(attr)

        # attribute access is stored as 1-element tuple
        self._chain.append((attr,))
        return self

    def __getitem__(self, slice):
        # slicing operation is stored as 2-element tuple
        self._chain.append((slice, None,))
        return self

    def __call__(self, *args, **kwargs):
        # method call is stored as 3-element tuple
        if not self._chain:
            # top-level call
            self._chain.append((None, args, kwargs))
        else:
            method_name = self._chain[-1][0]
            self._chain[-1] = (method_name, args, kwargs)
        return self

    def _proceed(self):
        """ Executes the collected chain and returns the result. """
        result = self._obj
        for op in self._chain:
            if len(op) == 1: # attribute
                result = getattr(result, op[0])
            elif len(op) == 2: # slice or index
                result = result[op[0]]
            elif len(op) == 3: # callable
                func = result if op[0] is None else getattr(result, op[0])
                result = func(*op[1], **op[2])
        return result

    def proceed(self, callback=None, worker=None):
        """
        Executes the collected chain using given worker and calls the
        callback with results.
        """
        worker = worker or self._worker
        worker.proceed(self, callback)


class Slacker(object):
    """
    Starts a new Postponed instance for every attribute access.
    Useful for wrapping existing classes into postponing proxies.
    """
    def __init__(self, obj, worker=None):
        self._obj = obj
        self._worker = worker

    def __getattr__(self, item):
        return getattr(Postponed(self._obj, self._worker), item)

    def __call__(self, *args, **kwargs):
        return Postponed(self._obj, self._worker).__call__(*args, **kwargs)


def proceed_pickled(pickled_postponed_obj):
    """
    Unpickles postponed object, proceeds it locally, then pickles the result
    and returns it. Raises SlackerException on errors.

    Useful for worker implementation.
    """
    try:
        postponed = pickle.loads(pickled_postponed_obj)
    except pickle.PicklingError, e:
        raise SlackerException(str(e))

    if not isinstance(postponed, Postponed):
        raise SlackerException('Pickled object is not an instance of Postponed')

    # TODO: better error handling
    result = postponed._proceed()
    return pickle.dumps(result, pickle.HIGHEST_PROTOCOL)
