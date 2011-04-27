from django.utils import unittest
from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from django.db import models
import pickle

from async_orm.chains import ChainProxy, ModelChainProxy

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


class ChainTest(unittest.TestCase):

    def assertRestored(self, chain, value):
        self.assertEqual(chain.restore(), value)

    def setUp(self):
        self.foo = Foo('foo')

    def _foo(self):
        # ChainProxy objects shouldn't be reused
        return ChainProxy(self.foo)

    def test_method_basic(self):
        self.assertRestored(self._foo().get_name(), 'foo')

    def test_method_args(self):
        chain = self._foo().xy(1, 2)
        self.assertRestored(chain, '1-2')

    def test_method_kwargs(self):
        self.assertRestored(self._foo().xy(y=2, x=1), '1-2')

    def test_attributes(self):
        self.assertRestored(self._foo().name, 'foo')

    def test_slicing(self):
        self.assertRestored(self._foo().name[0], 'f')

    def test_chaining(self):
        chain = self._foo().create_bar().bar.create_bar().bar.name[1:-1]
        self.assertRestored(chain, 'oo bar ba')

    def test_no_execution(self):
        self._foo().create_bar()
        self.assertFalse(hasattr(self.foo, 'bar'))

        self._foo().name
        self.assertFalse(self.foo.name_accessed)

        self.foo.name
        self.assertTrue(self.foo.name_accessed)


class ModelChainTest(DjangoTestCase):

    def setUp(self):
        self.user = User.objects.create_user('example', 'example@example.com')

    @property
    def AsyncUser(self):
        return ModelChainProxy(User)

    def test_restore(self):
        user = self.AsyncUser.objects.get(username='example')
        self.assertEqual(user.restore(), self.user)

    def test_pickling_unpickling(self):
        user = self.AsyncUser.objects.get(username='example')
        self.assertEqual(pickle.loads(user._pickled).restore(), self.user)
