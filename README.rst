================
django-async-orm
================

This app makes non-blocking django ORM calls possible.

Installation
============

::
    pip install "tornado >= 1.2"
    pip install django-async-orm

FIXME: this is not uploaded to pypi now

Overview
========

This app can be used for tornado + django integration: run tornado
as django management command (on a separate port) => all django code will be
available in tornado process; then use this library instead of
plain django ORM calls in Tornado handlers to make these calls non-blocking.

::

    from django.contrib.auth.models import User
    from async_orm.incarnations.http import AsyncWrapper

    AsyncUser = AsyncWrapper(User)

    # ...

    def process_data(self):
        # all the django orm syntax is supported here
        qs = AsyncUser.objects.filter(is_staff=True)[:5]
        qs.execute(self.on_ready)

    def on_ready(self, users):
        # do something with query result
        print users

or, with pep-342 syntax and adisp library (it is bundled)::

    from async_orm.vendor import adisp

    @adisp.process
    def process_data(self):
        qs = AsyncUser.objects.filter(is_staff=True)[:5]
        users = yield qs.fetch()
        print users

You still can't rely on third-party code that uses django ORM
in Tornado handlers but it is at least easy to reimplement it now
if necessary.

Currently the only implemented method for offloading query execution
from the ioloop is to execute the blocking code in a django view and
fetch results using tornado's AsyncHttpClient. This way it was possible
to get a simple implementation, easy deployment and a thread pool
(managed by webserver) for free. HTTP, however, can cause a
significant overhead.

Please dig into source code for more info, this README is totally
incomplete.

TODO: proper usage guide: how to configure django for this? how to deploy?

Configuration
=============

(async.incarnations.http.urls must be included in urls)

TODO: write this

Usage
=====

TODO

Contributing
============

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/kmike/django-async-orm/issues

Both hg and git pull requests are welcome!

* https://bitbucket.org/kmike/django-async-orm/
* https://github.com/kmike/django-async-orm/

Credits
=======

Inspiration:

* http://tornadogists.org/654157/
* https://github.com/satels/django-async-dbslayer/
* https://bitbucket.org/david/django-roa/

Third-party software: `adisp <https://code.launchpad.net/adisp>`_ (tornado
implementation is taken from `brukva <https://github.com/evilkost/brukva>`_).

License
=======

The license is MIT.

Bundled adisp library uses Simplified BSD License.
