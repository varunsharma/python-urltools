urltools
========

Some functions to parse and normalize URLs.


## Functions

### Normalize

    >>> urltools.normalize("Http://exAMPLE.com./foo")
    http://example.com/foo


### Encode

IDNA encoding (see RFC 3490).

    >>> urltools.encode("http://müller.de")
    'http://xn--mller-kva.de/'


### Parse

    >>> urltools.parse("http://example.co.uk/foo/bar?x=1#abc")
    ParseResult(scheme='http', username='', password='', subdomain='', domain='example', tld='co.uk', port='', path='/foo/bar', query='x=1', fragment='abc')
    >>> urltools.parse("www.example.co.uk/abc")
    ParseResult(scheme='', username='', password='', subdomain='', domain='', tld='', port='', path='www.example.co.uk/abc', query='', fragment='')

### Extract

The difference between `extract` and `parse` is that `parse` cares about relative
URLs and `extract` always tries to extract as much information as possible.

    >>> urltools.extract("www.example.co.uk/abc")
    ParseResult(scheme='', username='', password='', subdomain='www', domain='example', tld='co.uk', port='', path='/abc', query='', fragment='')


## Installation

You can install `urltools` from the Python Package Index (PyPI):

    pip install urltools

... or get the newest version directly from GitHub:

    pip install -e git://github.com/rbaier/urltools.git#egg=urltools


## Public Suffix List

`urltools` uses the Public Suffix List to split domain names correctly. E.g. the
TLD of `example.co.uk` would be `.co.uk` and not `.uk`.

I recommend to use a local copy of this list. Otherwise it will be downloaded
after each import of `urltools`.

    export PUBLIC_SUFFIX_LIST="/path/to/effective_tld_names.dat"

For more information see http://publicsuffix.org/


## Tests

To run the tests I use pytest:

    py.test -vrxs
