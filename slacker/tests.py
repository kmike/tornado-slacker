import pickle
from django.utils import unittest

from slacker.postpone import Postponed, Slacker

class Foo(object):

    def __init__(self, name):
        self._name = name
        self.name_accessed = False

    def create_bar(self):
        self.bar = Foo(self.name+' bar')
        return self

    def get_name(self):
        return self._name

    def xy(self, x, y):
        return "%s-%s" % (x,y)

    @property
    def name(self):
        self.name_accessed = True
        return self._name

FooSlacker = Slacker(Foo)

class PostponeTest(unittest.TestCase):

    def assertRestored(self, chain, value):
        self.assertEqual(chain._proceed(), value)

    def setUp(self):
        self.foo = FooSlacker('foo')

    def test_method_basic(self):
        self.assertRestored(self.foo.get_name(), 'foo')

    def test_method_args(self):
        chain = self.foo.xy(1, 2)
        self.assertRestored(chain, '1-2')

    def test_method_kwargs(self):
        self.assertRestored(self.foo.xy(y=2, x=1), '1-2')

    def test_attributes(self):
        self.assertRestored(self.foo.name, 'foo')

    def test_slicing(self):
        self.assertRestored(self.foo.name[0], 'f')

    def test_chaining(self):
        chain = self.foo.create_bar().bar.create_bar().bar.name[1:-1]
        self.assertRestored(chain, 'oo bar ba')

    def test_no_execution(self):
        real_foo = Foo('foo')
        foo = Postponed(real_foo)

        foo.create_bar()
        self.assertFalse(hasattr(real_foo, 'bar'))

        foo.name
        self.assertFalse(real_foo.name_accessed)

        real_foo.name
        self.assertTrue(real_foo.name_accessed)

    def test_top_level_callables(self):
        chain = Postponed(Foo)('bar')
        self.assertEqual(chain._proceed().name, 'bar')


class ModulesTest(unittest.TestCase):

    def assertRepickled(self, chain, value):
        repickled = pickle.loads(chain._pickled)
        self.assertEqual(repickled._proceed(), value)

    def test_modules(self):
        import string
        chain = Postponed(string).ascii_letters
        self.assertEqual(chain._proceed(), string.ascii_letters)

    def test_module_pickling_simple(self):
        import string
        chain = Postponed(string).ascii_letters
        self.assertRepickled(chain, string.ascii_letters)

    def test_module_pickling_dotted(self):
        import logging.handlers
        chain = Postponed(logging.handlers).SocketHandler
        self.assertRepickled(chain, logging.handlers.SocketHandler)

    def test_module_pickling_renamed(self):
        from logging import handlers as hh
        chain = Postponed(hh).SocketHandler
        self.assertRepickled(chain, hh.SocketHandler)

    def test_slacker(self):
        from logging import handlers as hh
        handlers = Slacker(hh)
        self.assertRepickled(handlers.SocketHandler, hh.SocketHandler)
        self.assertRepickled(handlers.DatagramHandler, hh.DatagramHandler)
