django-transaction-signals
##########################

tl;dr
=====

For the common use case of running code after the current transaction is
successfully committed:

- on Django >= 1.9, use the built-in on_commit_ hook
- on Django < 1.9, use `django-transaction-hooks`_

.. _on_commit: https://docs.djangoproject.com/en/stable/topics/db/transactions/#django.db.transaction.on_commit
.. _django-transaction-hooks: https://django-transaction-hooks.readthedocs.org/

Why?
====

Django doesn't provide transaction signals because they're a bad idea. Some of
the reasons will be apparent in the "Limitations" paragraph below. Other
reasons can be found in ticket 14051_ and on the django-developers mailing
list. However, I'm fed up with having this argument. People will shoot
themselves into the foot anyway.

This package will help you experience the problems
of transaction signals first-hand.

Use it at your own risk. I wouldn't.

.. _14051: https://code.djangoproject.com/ticket/14051

How?
====

Add ``'transaction_signals'`` to your ``INSTALLED_APPS`` setting.

This will monkey-patch Django's transaction management features.

You can then register receivers for transaction signals::

    from django.dispatch import receiver
    from transaction_signals import post_commit

    @receiver(post_commit)
    def print_commits(sender, **kwargs):
        print("COMMIT on %s" % sender)

Signals
=======

Signals are available in the ``transaction_signals`` package. Their semantics
are obvious, except when they aren't.

Connection signals:

- ``pre_open``
- ``post_open``
- ``pre_close``
- ``post_close``

Autocommit signals:

- ``pre_set_autocommit``
- ``post_set_autocommit``

Transaction signals:

- ``pre_commit``
- ``post_commit``
- ``pre_rollback``
- ``post_rollback``

Savepoint signals:

- ``pre_savepoint``
- ``post_savepoint``
- ``pre_savepoint_commit``
- ``post_savepoint_commit``
- ``pre_savepoint_rollback``
- ``post_savepoint_rollback``

``sender`` is the alias of the database connection e.g. ``'default'``. All
signals pass the database connection in the ``'connection'`` argument.
Furthermore,  ``pre/post_open`` provide a ``conn_params`` argument,
``pre/post_set_autocommit`` provide ``autocommit``, and
``pre/post_savepoint/_commit/_rollback`` provide ``savepoint_id``.

Limitations
===========

You cannot assume that ``pre/post_commit`` are sent whenever changes are
committed. Signals aren't sent when the connection is in autocommit mode,
which is the default_.

You cannot assume that ``pre/post_rollback`` are sent whenever changes are
cancelled. Closing the connection to the database triggers an implicit
rollback.

You cannot assume that ``pre/post_close`` are sent whenever an implicit
rollback happens. Losing the connection to the database also triggers an
implicit rollback.

After ``pre/post_savepoint`` is sent, you cannot assume that either
``pre/post_savepoint_commit`` or ``pre/post_savepoint_rollback`` will be sent
with the same ``savepoint_id``. The savepoint may be released or rolled back
together with an earlier savepoint or the entire transaction.

You cannot use ``pre/post_set_autocommit`` on SQLite. The ``sqlite3`` module
doesn't work in non-autocommit mode.

You cannot use ``pre/post_savepoint_commit`` on Oracle, Microsoft SQL Server,
or any other database that doesn't support releasing savepoints.

This is only the tip of the iceberg. I cannot recommend you use this package
if you learnt anything in this section. In fact, I cannot recommend it at all.

.. _default: https://docs.djangoproject.com/en/stable/topics/db/transactions/

Alternatives
============

Fortunately, if you want to add custom logic to Django's transaction handling,
you have several alternatives. They're much less likely to result in anger,
facepalms, insanity, loss of self-esteem, and other regrettable side effects.

You may put your custom logic:

* In a middleware, if you only care about transactions tied to requests when
  ``ATOMIC_REQUESTS`` is enabled.

* In a decorator that wraps ``atomic``, if you have more advanced needs,
  especially if you want to track partial commits and rollbacks.

* In a database backend, if you want tight control over database operations.
  Since there's no public API, you'll have to read the source and figure out
  how Django works, rather than blindly hooking to signals that may or may not
  be sent. django-transaction-hooks uses this technique.

License
=======

This package is released under a dual license: WTFPLv2 and GPLv2.

The distribution only includes the WTFPLv2 because the GPLv2 is too long.
