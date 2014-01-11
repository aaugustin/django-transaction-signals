# Use actual on-disk files to test opening and closing the connection.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'default.test.sqlite3',
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'other.test.sqlite3',
    },
}

INSTALLED_APPS = ['transaction_signals']

SECRET_KEY = 'WTF'
