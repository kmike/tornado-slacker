===============
tornado-slacker
===============

This package provides an easy API for moving the work out of
the tornado process.

Installation
============

::

    pip install "tornado >= 1.2"
    pip install tornado-slacker

FIXME: this is not uploaded to pypi now

Usage
=====

Please dig into source code for more info, this README is totally
incomplete.

TODO: proper usage guide: how to configure backend (e.g django) for this?
How to deploy?

Performance notes
=================

Currently the only implemented method for offloading query execution
from the ioloop is to execute the blocking code in a django view and
fetch results using tornado's AsyncHttpClient. This way it was possible
to get a simple implementation, easy deployment and a thread pool
(managed by webserver) for free.

IOLoop blocks on any CPU activity and making http requests plus
pickling/unpickling can cause a significant overhead here. So if the query
is fast (e.g. database primary key or index lookup, say 10ms) then it is
better to call the query in 'blocking' way: the overall blocking
time will be less than with 'async' approach because of reduced
computations amount.

tornado-slacker unpickles the received results and unpickling can be
CPU-intensive so it is better to return as little as possible from
postponed chains.

Contributing
============

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/kmike/tornado-slacker/issues

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
