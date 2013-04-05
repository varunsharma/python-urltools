# -*- coding: utf-8 -*-

import tymer

from urltools.urltools import normalize, parse, extract, encode, split
from urltools.urltools import _assemble


setup_timeit = """
from __main__ import normalize, parse, extract, encode, split
from __main__ import _assemble
"""


@tymer.skip
def timeit_parse():
    print "parse", tymer.t('parse("http://example.com")')


#@tymer.skip
def timeit__assemble():
    stmt = """
    parts = extract("http://www.example.com:8080/abc?x=1#rt")
    _assemble(parts)
    """
    print "_assemble", tymer.t(stmt)


if __name__ == '__main__':
    tymer.run()
