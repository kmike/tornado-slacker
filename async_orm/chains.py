import pprint
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db.models.loading import get_model


class AsyncOrmException(Exception):
    pass


class ChainProxy(object):
    """
    Stores attribute, call and slice chain without actully
    calling methods, accessing attributes and performing slicing.

    Collecting the access to private methods and attributes
    (beginning with __two_underscores) is not supported.

    FIXME: '_obj', '_chain' and 'restore' attributes of original
    object are replaced with the ones from this proxy.
    """

    def __init__(self, obj, **kwargs):
        self._obj = obj
        self._chain = []
        self._extra = kwargs

    def __getattr__(self, attr):
        # pickle.dumps internally checks if __getnewargs__ is defined
        # and thus returning ChainProxy object instead of
        # raising AttributeError breaks pickling. Returning self instead
        # of raising an exception for private attributes can possible
        # break something else so the access to private methods and attributes
        # is not overriden at all.
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
        method_name = self._chain[-1][0]
        self._chain[-1] = (method_name, args, kwargs)
        return self

    def restore(self):
        """ Executes and returns the stored chain. """
        result = self._obj
        for op in self._chain:
            if len(op) == 1: # attribute
                result = getattr(result, op[0])
            elif len(op) == 2: # slice or index
                result = result[op[0]]
            elif len(op) == 3: # method
                result = getattr(result, op[0])(*op[1], **op[2])
        return result

    def __repr__(self):
        return "%s: %s" % (self._obj, pprint.pformat(self._chain))


class ModelChainProxy(ChainProxy):
    """
    Adds support for pickling when proxy is applied to
    django.db.models.Model subclass.

    This handles QuerySet method arguments like Q objects,
    F objects and aggregate functions (e.g. Count) properly,
    but can break on QuerySets as arguments (queryset will be executed).

    Why not follow the advice from django docs and just pickle queryset.query?
    http://docs.djangoproject.com/en/dev/ref/models/querysets/#pickling-querysets

    The advice is limited to QuerySets. With ModelChainProxy it is possible
    to pickle any ORM calls including ones that don't return QuerySets:
    http://docs.djangoproject.com/en/dev/ref/models/querysets/#methods-that-do-not-return-querysets

    Moreover, using custom managers and model methods, as well as returning model
    attributes, is fully supported. This allows user to execute any
    orm-related code (e.g. populating the instance and saving it) in
    non-blocking manner: just write the code as a model or manager method.
    """
    def _model_data(self):
        meta = self._obj._meta
        return meta.app_label, meta.object_name

    def __getstate__(self):
        return dict(
            chain = self._chain,
            model_class = self._model_data()
        )

    def __setstate__(self, dict):
        self._chain = dict['chain']
        model_class = get_model(*dict['model_class'])
        self._obj = model_class

    @property
    def _pickled(self):
        return pickle.dumps(self, pickle.HIGHEST_PROTOCOL)

    def __repr__(self):
        app, model = self._model_data()
        return "%s.%s: %s" % (app, model, pprint.pformat(self._chain))


class ProxyWrapper(object):
    """
    Creates a new ChainProxy subclass instance on every attribute access.
    Useful for wrapping existing classes into chain proxies.
    """
    proxy_class = ModelChainProxy

    def __init__(self, cls, **kwargs):
        self._cls = cls
        self._extra = kwargs

    def __getattr__(self, item):
        return getattr(self.proxy_class(self._cls, **self._extra), item)


def repickle_chain(pickled_data):
    """
    Unpickles and executes pickled chain, then pickles the result
    and returns it. Raises AsyncOrmException on errors.
    """
    try:
        chain = pickle.loads(pickled_data)
    except pickle.PicklingError, e:
        raise AsyncOrmException(str(e))

    if not isinstance(chain, ChainProxy):
        raise AsyncOrmException('Pickled query is not an instance of ChainProxy')

    # TODO: better error handling
    restored = chain.restore()
    data = pickle.dumps(restored, pickle.HIGHEST_PROTOCOL)
    return data
