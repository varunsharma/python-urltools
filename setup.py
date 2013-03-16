#!/usr/bin/env python

from setuptools import setup, find_packages

import urltools

setup(name='urltools',
	  version=urltools.__version__,
	  description='url tools',
	  author='Roderick Baier',
	  author_email='roderick.baier@gmail.com',
	  url='https://github.com/rbaier/urltools',
	  packages=find_packages(exclude=['tests']))