===============
tornado-slacker
===============

This package provides an easy API for moving the work out of
the tornado process / event loop.

Currently implemented methods are:

* execute the code in another server's http hook
  (django implementation is included);
* execute the code in a separate thread;
* dummy immediate execution.

API example::

    from django.contrib.auth.models import User
    from slacker import adisp
    from slacker import Slacker
    from slacker.workers.django import DjangoWorker

    AsyncUser = Slacker(User, DjangoWorker())

    @adisp.process
    def process_data():

        # all the django ORM is supported; the query will be executed
        # on remote end, this will not block the IOLoop
        qs = AsyncUser.objects.filter(is_staff=True)[:5]

        # execute the query and get the results
        users = yield qs.fetch()
        print users

(pep-342 syntax and adisp library are optional, callback-style code
is also supported)


Installation
============

::

    pip install tornado-slacker

Slackers
========

Slackers are special objects that are collecting operations (attribute
access, calls, slicing) without actually executing them. Callable arguments
must be picklable. Slackers also provide a method to apply the collected
operations to a base object.

Any picklable object (including top-level functions and classes) can
be wrapped into Slacker, e.g.::

    from slacker import adisp
    from slacker import Slacker
    from slacker.workers import ThreadWorker

    def task(param1, param2):
        # do something blocking and io-bound
        return results

    async_task = Slacker(task, ThreadWorker())

    # pep-342-style
    @adisp.process
    def process_data():
        results = yield async_task('foo', 'bar').fetch()
        print results

    # callback style
    def process_data2():
        async_task('foo', 'bar').proceed(on_result)

    def on_result(results):
        print results


Workers
=======

Workers are classes that decides how and where the work should be done:

* ``slacker.workers.local.DummyWorker`` executes code in-place (this
  is blocking);

* ``slacker.workers.local.ThreadWorker`` executes code in a thread from
  a thread pool;

* ``slacker.workers.http.HttpWorker`` pickles the slacker, makes an async
  http request with this data to a given server hook and expects it
  to execute the code and return pickled results;

  .. note::

      IOLoop blocks on any CPU activity and making http requests plus
      unpickling the returned result can cause a significant overhead
      here. So if the query is fast (e.g. database primary key or index
      lookup, say 10ms) then it may be better not to use tornado-slacker
      and call the query in 'blocking' way: the overall blocking time
      may be less than with 'async' approach because of reduced
      computations amount.

      It is also wise to return as little as possible if HttpWorker is used.


* ``slacker.workers.django.DjangoHttpWorker`` is just a HttpWorker with
  default values for use with bundled django remote server hook implementation
  (``slacker.django_backend``).

  In order to enable django hook, include 'slacker.django_backend.urls'
  into urls.py and add SLACKER_SERVER option with server address to
  settings.py.

  SLACKER_SERVER is '127.0.0.1:8000' by default so this should work for
  development server out of box.

  .. warning::

      Do not expose django server hook to public, this is insecure!
      The best way is to configure additional server instance to listen
      some local port (e.g. bind it to the default 127.0.0.1:8000 address).

  .. note::

      Django's QuerySet arguments like Q, F objects, aggregate and annotate
      functions (e.g. Count) are picklable so tornado-slacker can handle
      them fine::

          AsyncAuthor = Slacker(Author, DjangoWorker())

          # ...
          qs = AsyncAuthor.objects.filter(
                  Q(name='vasia') or Q(is_great=True)
               ).values('name').annotate(average_rating=Avg('book__rating'))[:10]

          authors = yield qs.fetch()

      Using slacker.Slacker is better than pickling queryset.query
      (as adviced at http://docs.djangoproject.com/en/dev/ref/models/querysets/#pickling-querysets)
      because this allows to pickle any ORM calls including ones that
      don't return QuerySets (http://docs.djangoproject.com/en/dev/ref/models/querysets/#methods-that-do-not-return-querysets)::

          yield AsyncUser.objects.create_superuser('foo').fetch()

      Moreover, slacker.Slacker adds transparent support for remote invocation
      of custom managers and model methods, returning just the model instance
      attributes, etc.


Contributing
============

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker:

* https://github.com/kmike/tornado-slacker/issues

Source code:

* https://bitbucket.org/kmike/tornado-slacker/
* https://github.com/kmike/tornado-slacker/

Both hg and git pull requests are welcome!

Credits
=======

Inspiration:

* https://github.com/satels/django-async-dbslayer/
* https://bitbucket.org/david/django-roa/
* http://tornadogists.org/654157/

Third-party software: `adisp <https://code.launchpad.net/adisp>`_ (tornado
adisp implementation is taken from
`brukva <https://github.com/evilkost/brukva>`_).

License
=======

The license is MIT.

Bundled adisp library uses Simplified BSD License.
