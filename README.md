urltools
========

[![version](https://pypip.in/v/urltools/badge.png?style=flat)](https://pypi.python.org/pypi/urltools)
[![Supported Python versions](https://pypip.in/py_versions/urltools/badge.svg?style=flat)](https://pypi.python.org/pypi/urltools/)
[![format](https://pypip.in/format/urltools/badge.png?style=flat)](https://pypi.python.org/pypi/urltools)
[![downloads](https://pypip.in/d/urltools/badge.png?style=flat)](https://pypi.python.org/pypi/urltools)
[![license](https://pypip.in/license/urltools/badge.png?style=flat)](https://pypi.python.org/pypi/urltools)

Some functions to parse and normalize URLs.


## Functions

### Normalize

    >>> urltools.normalize("Http://exAMPLE.com./foo")
    http://example.com/foo

Rules that are applied to normalize a URL:

* tolower scheme
* tolower host (also works with IDNs)
* remove default port
* remove ':' without port
* remove DNS root label
* unquote path, query, fragment
* collapse path (remove '//', '/./', '/../')
* sort query params and remove params without value


### Parse

The result of `parse` and `extract` is a `URL` named tuple that contains
`scheme`, `username`, `password`, `subdomain`, `domain`, `tld`, `port`, `path`,
`query`, `fragment` and the original `url` itself.

    >>> urltools.parse("http://example.co.uk/foo/bar?x=1#abc")
    URL(scheme='http', username='', password='', subdomain='', domain='example',
    tld='co.uk', port='', path='/foo/bar', query='x=1', fragment='abc',
    url='http://example.co.uk/foo/bar?x=1#abc')

If the `scheme` is missing `parse` interprets the URL as relative.

    >>> urltools.parse("www.example.co.uk/abc")
    URL(scheme='', username='', password='', subdomain='', domain='', tld='',
    port='', path='www.example.co.uk/abc', query='', fragment='',
    url='www.example.co.uk/abc')


### Extract

`extract` does not care about relative URLs and always tries to extract as much
information as possible.

    >>> urltools.extract("www.example.co.uk/abc")
    URL(scheme='', username='', password='', subdomain='www', domain='example',
    tld='co.uk', port='', path='/abc', query='', fragment='',
    url='www.example.co.uk/abc')


### Additional functions

Besides the already described main functions `urltools` has some more functions
to manipulate segments of a URL or create new URLs.

* `construct` a new URL from parts

        >>> construct(URL('http', '', '', '', 'example', 'com', '/abc', 'x=1',
        ... 'foo', None))
        'http://example.com/abc?x=1#foo'

* `compare` two urls to check if they are the same

        >>> compare("http://examPLe.com:80/abc?x=&b=1",
        ... "http://eXAmple.com/abc?b=1")
        True

* `encode` (IDNA, see RFC 3490)

        >>> urltools.encode("http://müller.de")
        'http://xn--mller-kva.de/'

* `normalize_host`
* `normalize_path`

        >>> normalize_path("/a/b/../../c")
        '/c'

* `normalize_query`

        >>> normalize_query("x=1&y=&z=3")
        'x=1&z=3'

* `normalize_fragment`
* `unquote`
* `split` (basically the same as `urlparse.urlparse`)

        >>> split("http://www.example.com/abc?x=1&y=2#foo")
        SplitResult(scheme='http', netloc='www.example.com', path='/abc',
        query='x=1&y=2', fragment='foo')

* `split_netloc`

        >>> split_netloc("foo:bar@www.example.com:8080")
        ('foo', 'bar', 'www.example.com', '8080')

* `split_host`

        >>> split_host("www.example.ac.at")
        ('www', 'example', 'ac.at')



## Installation

You can install `urltools` from the Python Package Index (PyPI):

    pip install urltools

... or get the newest version directly from GitHub:

    pip install -e git://github.com/rbaier/python-urltools.git#egg=urltools



## Public Suffix List

`urltools` uses the Public Suffix List to split domain names correctly. E.g. the
TLD of `example.co.uk` would be `.co.uk` and not `.uk`.

I recommend to use a local copy of this list. Otherwise it will be downloaded
after each import of `urltools`.

    export PUBLIC_SUFFIX_LIST=/path/to/effective_tld_names.dat

For more information see http://publicsuffix.org/



## Tests

tox and pytest are used for testing. Simply install tox and run it:

    pip install tox
    tox
