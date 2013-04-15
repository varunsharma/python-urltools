urltools
========

Some functions to parse and normalize URLs.


## Functions

### Normalize

    >>> urltools.normalize("Http://exAMPLE.com./foo")
    http://example.com/foo

* tolower scheme
* tolower host
* remove HTTP default port (80)
* remove ':' without port
* remove DNS root label
* unquote path
* collapse path (remove '//', '/./', '/../')
* sort query params and remove params without value


### Parse

The result of `parse` and `extract` is a `ParseResult` named tuple that contains `scheme`, `username`, `password`, `subdomain`, `domain`, `tld`, `port`, `path`, `query` and `fragment`.

    >>> urltools.parse("http://example.co.uk/foo/bar?x=1#abc")
    ParseResult(scheme='http', username='', password='', subdomain='', domain='example', tld='co.uk', port='', path='/foo/bar', query='x=1', fragment='abc')

If the `scheme` is missing `parse` interprets the URL as relative.

    >>> urltools.parse("www.example.co.uk/abc")
    ParseResult(scheme='', username='', password='', subdomain='', domain='', tld='', port='', path='www.example.co.uk/abc', query='', fragment='')

### Extract

`extract` does not care about relative URLs and always tries to extract as much information as possible.

    >>> urltools.extract("www.example.co.uk/abc")
    ParseResult(scheme='', username='', password='', subdomain='www', domain='example', tld='co.uk', port='', path='/abc', query='', fragment='')

### Encode

IDNA encoding (see RFC 3490).

    >>> urltools.encode("http://müller.de")
    'http://xn--mller-kva.de/'


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
