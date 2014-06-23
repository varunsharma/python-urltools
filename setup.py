#!/usr/bin/env python

from setuptools import setup, find_packages

from urltools import urltools

setup(
    name = 'urltools',
    version = urltools.__version__,
    description = 'Some functions to parse and normalize URLs.',
    author = 'Roderick Baier',
    author_email = 'roderick.baier@gmail.com',
    license = 'MIT',
    url = 'https://github.com/rbaier/urltools',
    packages = find_packages(exclude=['tests'])
)
