urltools
========

Some functions to parse and normalize URLs.


## Example

Normalize URL

    >>> urltools.normalize("Http://exAMPLE.com./foo")
    http://example.com/foo


## Installation

   pip install -e git://github.com/rbaier/urltools.git#egg=urltools


## Public Suffix List

To use a local copy of the Public Suffix List:

    export PUBLIC_SUFFIX_LIST="/path/to/effective_tld_names.dat"

For more information see http://publicsuffix.org/
