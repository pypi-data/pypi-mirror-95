v3.2.1
======

Refreshed package metadata.

v3.2.0
======

Switched to PEP 420 for ``jaraco`` namespace.

v3.1.0
======

Added ``except_`` decorator.

v3.0.1
======

#14: Removed unnecessary compatibility libraries in testing.

v3.0.0
======

Require Python 3.6 or later.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.20
====

Added ``save_method_args``, adopted from ``irc.functools``.

1.19
====

Added ``.reset`` support to ``once``.

1.18
====

Add ``result_invoke`` decorator.

1.17
====

Add ``retry`` decorator.

1.16
====

#7: ``retry_call`` now accepts infinity for the ``retries``
parameter.

1.15.2
======

Refresh packaging.

1.15.1
======

Fix assign_params on Python 2.

1.15
====

Add ``assign_params`` function.

1.14
====

Add ``pass_none`` decorator function.

1.13
====

Add ``print_yielded`` func implementing the func of the same
name found in autocommand docs.

1.12
====

Issue #6: Added a bit of documentation and xfail tests showing
that the ``method_cache`` can't be used with other decorators
such as ``property``.

1.11
====

Include dates and links in changelog.

1.10
====

Use Github for continuous deployment to PyPI.

1.9
===

Add ``retry_call``, a general-purpose function retry mechanism.
See ``test_functools`` for tests and example usage.

1.8
===

More generous handling of missing lru_cache when installed on
Python 2 and older pip. Now all functools except ``method_cache``
will continue to work even if ``backports.functools_lru_cache``
is not installed. Also allows functools32 as a fallback if
available.

1.7
===

Moved hosting to github.

1.6
===

``method_cache`` now accepts a cache_wrapper parameter, allowing
for custom parameters to an ``lru_cache`` or an entirely different
cache implementation.

Use ``backports.functools_lru_cache`` to provide ``lru_cache`` for
Python 2.

1.5
===

Implement ``Throttler`` as a descriptor so it may be used to decorate
methods. Introduces ``first_invoke`` function.

Fixed failure in Throttler on Python 2 due to improper use of integer
division.

1.4
===

Added ``Throttler`` class from `irc <https://bitbucket.org/jaraco/irc>`_.

1.3
===

Added ``call_aside`` decorator.

1.2
===

Added ``apply`` decorator.

1.0
===

Initial release drawn from jaraco.util.
