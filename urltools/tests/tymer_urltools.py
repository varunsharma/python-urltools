# -*- coding: utf-8 -*-

from tymer import t, run, skip

from urltools.urltools import normalize, parse, extract, encode, split
from urltools.urltools import _assemble


setup_tymer = """
from __main__ import normalize, parse, extract, encode, split
from __main__ import _assemble
"""


#@skip
def tymer_parse():
    t('parse("http://example.com")')


#@skip
def tymer__assemble():
    stmt = """
    parts = extract("http://www.example.com:8080/abc?x=1#rt")
    _assemble(parts)
    """
    t(stmt)


if __name__ == '__main__':
    run()
