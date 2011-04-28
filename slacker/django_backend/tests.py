import pickle

from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User

from slacker.postpone import Postponed

class DjangoQueryPostponeTest(DjangoTestCase):

    def setUp(self):
        self.user = User.objects.create_user('example', 'example@example.com')

    @property
    def AsyncUser(self):
        return Postponed(User)

    def test_restore(self):
        user_query = self.AsyncUser.objects.get(username='example')
        self.assertEqual(user_query._proceed(), self.user)

    def test_pickling_unpickling(self):
        user_query = self.AsyncUser.objects.get(username='example')
        self.assertEqual(pickle.loads(user_query._pickled)._proceed(), self.user)

