export PYTHONPATH:=.:$(PYTHONPATH)
export DJANGO_SETTINGS_MODULE:=transaction_signals.test_settings

test:
	django-admin.py test transaction_signals
