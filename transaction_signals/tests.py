from contextlib import contextmanager
from unittest import TestCase

from django.db import DEFAULT_DB_ALIAS, connection, connections, transaction
from django.dispatch import receiver


root_package = __import__(__name__.partition('.')[0])


def register_receiver(signal_name):
    @receiver(getattr(root_package, signal_name), weak=False)
    def log_signal(sender, **kwargs):
        TransactionSignalTests.store_signal(
            (signal_name, kwargs))


for signal_name in dir(root_package):
    if signal_name.startswith('__') or signal_name.startswith('test'):
        continue
    register_receiver(signal_name)


class TransactionSignalTests(TestCase):

    @classmethod
    @contextmanager
    def store_signals(cls):
        cls.signals = []
        try:
            yield cls.signals
        finally:
            del cls.signals

    @classmethod
    def store_signal(cls, signal):
        try:
            cls.signals.append(signal)
        except AttributeError:
            pass

    @staticmethod
    def run_query(alias=DEFAULT_DB_ALIAS):
        connections[alias].cursor().execute("SELECT 0")

    @classmethod
    def setUpClass(cls):
        for alias in connections:
            cls.run_query(alias)

    def tearDown(self):
        for alias in connections:
            if connections[alias].connection is None:
                raise RuntimeError("Test closed connection '%s'!" % alias)

    def test_open_and_set_autocommit(self):
        connection.close()
        with self.store_signals() as signals:
            self.run_query()
        self.assertEqual(len(signals), 4)
        self.assertEqual('pre_open', signals[0][0])
        self.assertEqual('post_open', signals[1][0])
        self.assertEqual('pre_set_autocommit', signals[2][0])
        self.assertEqual('post_set_autocommit', signals[3][0])

    def test_close(self):
        with self.store_signals() as signals:
            connection.close()
        self.run_query()
        self.assertEqual(len(signals), 2)
        self.assertEqual('pre_close', signals[0][0])
        self.assertEqual('post_close', signals[1][0])

    def test_commit(self):
        with self.store_signals() as signals:
            with transaction.atomic():
                self.run_query()
        self.assertEqual(len(signals), 2)
        self.assertEqual('pre_commit', signals[0][0])
        self.assertEqual('post_commit', signals[1][0])

    def test_rollback(self):
        with self.store_signals() as signals:
            with self.assertRaises(RuntimeError):
                with transaction.atomic():
                    self.run_query()
                    raise RuntimeError
        self.assertEqual(len(signals), 2)
        self.assertEqual('pre_rollback', signals[0][0])
        self.assertEqual('post_rollback', signals[1][0])

    def test_savepoint_and_savepoint_commit(self):
        with transaction.atomic():
            with self.store_signals() as signals:
                with transaction.atomic():
                    self.run_query()
        self.assertEqual(len(signals), 4)
        # One would expect pre/post_set_autocommit, but, sqlite3, sigh.
        self.assertEqual('pre_savepoint', signals[0][0])
        self.assertEqual('post_savepoint', signals[1][0])
        self.assertEqual('pre_savepoint_commit', signals[2][0])
        self.assertEqual('post_savepoint_commit', signals[3][0])

    def test_savepoint_and_savepoint_rollback(self):
        with transaction.atomic():
            with self.store_signals() as signals:
                with self.assertRaises(RuntimeError):
                    with transaction.atomic():
                        self.run_query()
                        raise RuntimeError
        self.assertEqual(len(signals), 4)
        # One would expect pre/post_set_autocommit, but, sqlite3, sigh.
        self.assertEqual('pre_savepoint', signals[0][0])
        self.assertEqual('post_savepoint', signals[1][0])
        self.assertEqual('pre_savepoint_rollback', signals[2][0])
        self.assertEqual('post_savepoint_rollback', signals[3][0])

    def test_open_and_set_autocommit_other(self):
        connections['other'].close()
        with self.store_signals() as signals:
            self.run_query('other')
        self.assertEqual(len(signals), 4)
        self.assertEqual('pre_open', signals[0][0])
        self.assertEqual('post_open', signals[1][0])
        self.assertEqual('pre_set_autocommit', signals[2][0])
        self.assertEqual('post_set_autocommit', signals[3][0])

    def test_commit_other(self):
        with self.store_signals() as signals:
            with transaction.atomic('other'):
                self.run_query('other')
        self.assertEqual(len(signals), 2)
        self.assertEqual('pre_commit', signals[0][0])
        self.assertEqual('post_commit', signals[1][0])
