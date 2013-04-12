# -*- coding: utf-8 -*-

import posixpath
from urlparse import urlparse

import tldextract
from tymer import t, run, skip

from urltools.urltools import normalize, parse, extract, encode, split
from urltools.urltools import assemble, _clean_netloc, normalize_path, split_netloc
from urltools.urltools import _get_public_suffix_list, normalize_path2


setup_tymer = """
from __main__ import normalize, parse, extract, encode, split
from __main__ import assemble, _clean_netloc, normalize_path, split_netloc
from __main__ import urlparse, posixpath
from __main__ import tldextract
from __main__ import _get_public_suffix_list, normalize_path2
"""


@skip
def tymer_split_netloc():
    t('split_netloc("foo:bar@www.example.com:8080")')


@skip
def tymer__get_public_suffix_list():
    t('_get_public_suffix_list()')


@skip
def tymer_split():
    t('urlparse("http://example.com")')
    t('split("http://example.com")')


#@skip
def tymer_normalize_path():
    t('normalize_path("/foo////../bar/./a/b/")')
    t('posixpath.normpath("/foo////../bar/./a/b/")')
    t('normalize_path2("/foo////../bar/./a/b/")')


@skip
def tymer_normalize():
    t('normalize("http://WwW.exAmple.com./a/b/..////c?x=1#abc")')


@skip
def tymer__clean_netloc():
    t('_clean_netloc("ПриМЕр.Рф")')
    t('_clean_netloc("example.com:")')
    t('_clean_netloc("fOO.baR.example.com")')


@skip
def tymer_parse():
    t('parse("http://example.com")')
    t('extract("http://example.com")')
    t('urlparse("http://example.com")')
    t('tldextract.extract("http://example.com")')


@skip
def tymer_assemble():
    stmt = """
    parts = extract("http://www.example.com:8080/abc?x=1#rt")
    assemble(parts)
    """
    t(stmt)


if __name__ == '__main__':
    run()
