from __future__ import unicode_literals

import codecs
import os.path

import setuptools

root_dir = os.path.abspath(os.path.dirname(__file__))

description = "Transaction signals for Django. Don't use this!"

with codecs.open(os.path.join(root_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='django-transaction-signals-do-not-use',
    version='1.0',
    description=description,
    long_description=long_description,
    url='https://github.com/aaugustin/django-transaction-signals',
    author='Aymeric Augustin',
    author_email='aymeric.augustin@m4x.org',
    license='WTFPLv2 and GPLv2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=[
        'transaction_signals',
    ],
)
