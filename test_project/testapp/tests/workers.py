

from tornado.testing import AsyncHTTPTestCase
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

from django.core.handlers.wsgi import WSGIHandler
from django.test import TransactionTestCase as DjangoTestCase
from django.contrib.auth.models import User

from slacker import Slacker, adisp
from slacker.workers import ThreadWorker, DjangoWorker

class BaseWorkerTest(AsyncHTTPTestCase, DjangoTestCase):

    SlackerClass = Slacker(User)

    def setUp(self):
        self.user = User.objects.create_user('example', 'example@example.com')
        self.res = None
        super(BaseWorkerTest, self).setUp()

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return WSGIContainer(WSGIHandler())

    @adisp.process
    def get_user(self):
        self.res = yield self.SlackerClass.objects.get(username=self.user.username)
        self.stop()

    def test_get_user(self):
        self.get_user()
        self.wait()
        self.assertEqual(self.res, self.user)


class DjangoWorkerTest(BaseWorkerTest):
    def setUp(self):
        super(DjangoWorkerTest, self).setUp()
        self.SlackerClass = Slacker(User, DjangoWorker(self.get_url('')))


class ThreadedWorkerTest(BaseWorkerTest):
    SlackerClass = Slacker(User, ThreadWorker())

