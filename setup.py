#!/usr/bin/env python

from setuptools import setup, find_packages

from urltools import urltools

setup(
    name='urltools2',
    version=urltools.__version__,
    description='Some functions to parse and normalize URLs.',
    long_description='Some functions to parse and normalize URLs.',
    author='Roderick Baier, Varun Sharma',
    author_email='roderick.baier@gmail.com, varunsharmalive@gmail.com',
    license='MIT',
    url='https://github.com/varunsharma/python-urltools',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ]
)
