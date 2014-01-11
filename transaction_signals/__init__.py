from django.db import connections

from .monkey import *
from .signals import *

# Monkey-patch Django as a side effect of an import \o/

for connection in connections.all():
    patch(connection)


del connection, connections, monkey, patch, signals
