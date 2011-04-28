from django.core.urlresolvers import reverse
from slacker.postpone import PostponeWrapper
from slacker.workers.http import TornadoAsyncHttpWorker
from slacker.django_backend.conf import SLACKER_SERVER

def get_async(obj, server=None, path=None):
    """
    Allows async iteractions with given object by moving actual work
    to a django server.

    Example::

        # urls.py
        # ...
        urlpatterns = patterns('',
            # ...
            url(r'sakd3j7fhg8sdkjlk09fhgksdjhfg', include('slacker.django_backend.urls')),
            # ...
        )

        # your tornado app code
        from django.contrib.auth.models import User
        from slacker.django_backend import get_async

        AsyncUser = get_async(User)

        # ...

        def process_data(self):
            # all the django orm syntax is supported here, including
            # slicing, Q and F objects, aggregate functions like Count,
            # custom managers and model methods and attributes

            async_qs = AsyncUser.objects.filter(is_staff=True)[:5]
            async_qs.proceed(self.on_ready)

        def on_ready(self, users):
            # do something with query result
            print users

    or even better, with pep-342 syntax and adisp library (it is bundled)::

        from slacker import adisp

        # ...

        @adisp.process
        def process_data(self):
            qs = AsyncUser.objects.filter(is_staff=True)[:5]
            users = yield qs.fetch()
            print users


    with functions (they must be top-level)::

        def task(param1, param2):
            # do something costly and blocking
            return result

        # do not use decorator syntax here, the original function is necessary
        async_task = get_async(task)

        # ...

        @adisp.process
        def process_data(self):
            results = yield async_task('foo', 'bar')
            print results

    """
    server = server or SLACKER_SERVER
    path = path or reverse('slacker-execute')
    worker = TornadoAsyncHttpWorker(server, path)
    return PostponeWrapper(obj, worker)
