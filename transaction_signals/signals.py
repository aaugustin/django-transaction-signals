from django.dispatch import Signal


pre_open = Signal(providing_args=["connection", "conn_params"])
post_open = Signal(providing_args=["connection", "conn_params"])

pre_set_autocommit = Signal(providing_args=["connection", "autocommit"])
post_set_autocommit = Signal(providing_args=["connection", "autocommit"])

pre_close = Signal(providing_args=["connection"])
post_close = Signal(providing_args=["connection"])

pre_commit = Signal(providing_args=["connection"])
post_commit = Signal(providing_args=["connection"])

pre_rollback = Signal(providing_args=["connection"])
post_rollback = Signal(providing_args=["connection"])

pre_savepoint = Signal(providing_args=["connection", "savepoint_id"])
post_savepoint = Signal(providing_args=["connection", "savepoint_id"])

pre_savepoint_commit = Signal(providing_args=["connection", "savepoint_id"])
post_savepoint_commit = Signal(providing_args=["connection", "savepoint_id"])

pre_savepoint_rollback = Signal(providing_args=["connection", "savepoint_id"])
post_savepoint_rollback = Signal(providing_args=["connection", "savepoint_id"])


__all__ = [name for name, obj in globals().items() if isinstance(obj, Signal)]
