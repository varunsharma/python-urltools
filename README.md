urltools
========

Some functions to parse and normalize URLs.


## Functions

### Normalize:

    >>> urltools.normalize("Http://exAMPLE.com./foo")
    http://example.com/foo

### Parse

    >>> urltools.parse("http://example.co.uk/foo/bar?x=1#abc")
    Result(scheme='http', domain='example', tld='co.uk', port='80', path='/foo/bar', query='x=1', fragment='abc')


## Installation

    pip install -e git://github.com/rbaier/urltools.git#egg=urltools


## Public Suffix List

urltools uses the Public Suffix List to split domain names correctly. E.g. the
correct TLD of `example.co.uk` would be `.co.uk` and not `.uk`.

To use a local copy of the Public Suffix List:

    export PUBLIC_SUFFIX_LIST="/path/to/effective_tld_names.dat"

For more information see http://publicsuffix.org/


## Tests

To run the tests I use pytest:

    py.test -vrxs
