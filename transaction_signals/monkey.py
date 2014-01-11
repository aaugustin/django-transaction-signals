from functools import wraps

from . import signals


__all__ = ['patch']


def patch_method(connection, method_name, args_names, signal_name):
    pre_signal = getattr(signals, 'pre_%s' % signal_name)
    post_signal = getattr(signals, 'post_%s' % signal_name)
    old_method = getattr(connection, method_name)
    @wraps(old_method)
    def new_method(self, *args):
        kwargs = dict(zip(args_names, args))
        kwargs['connection'] = self
        pre_signal.send(self.alias, **kwargs)
        result = old_method(self, *args)
        post_signal.send(self.alias, **kwargs)
        return result
    setattr(connection, method_name, new_method)


def patch(connection):
    connection = type(connection)
    if getattr(connection, '_patched_for_transaction_signals', False):
        return

    for signal_name, method_name, args_names in (
        ('open', 'get_new_connection', ('conn_params',)),
        ('set_autocommit', '_set_autocommit', ()),
        ('close', '_close', ()),
        ('commit', '_commit', ()),
        ('rollback', '_rollback', ()),
        ('savepoint', '_savepoint', ('savepoint_id',)),
        ('savepoint_commit', '_savepoint_commit', ('savepoint_id',)),
        ('savepoint_rollback', '_savepoint_rollback', ('savepoint_id',)),
    ):
        patch_method(connection, method_name, args_names, signal_name)

    connection._patched_for_transaction_signals = True
