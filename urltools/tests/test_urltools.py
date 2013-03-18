#import pytest

from urltools import normalize, parse
from urltools.urltools import _clean_netloc, _get_public_suffix_list


def test_normalize():
    assert normalize("http://example.com") == "http://example.com/"
    assert normalize("http://example.com/") == "http://example.com/"
    assert normalize("https://example.com/") == "https://example.com/"
    assert normalize("hTTp://example.com/") == "http://example.com/"
    assert normalize("http://ExAMPLe.COM/") == "http://example.com/"
    assert normalize("http://example.com./") == "http://example.com/"
    assert normalize("http://example.com:80/") == "http://example.com/"
    assert normalize("http://example.com/#") == "http://example.com/"

    assert normalize("http://example.com:8080/") == "http://example.com:8080/"

    assert normalize("http://www.example.com/") == "http://www.example.com/"
    assert normalize("http://www.example.com") == "http://www.example.com/"
    assert normalize("http://foo.bar.example.com/") == "http://foo.bar.example.com/"

    assert normalize("http://example.com/a") == "http://example.com/a"
    assert normalize("http://example.com/a/b/c") == "http://example.com/a/b/c"

    assert normalize("http://example.com/?x=1") == "http://example.com/?x=1"
    assert normalize("http://example.com/a?x=1") == "http://example.com/a?x=1"
    assert normalize("http://example.com/a?x=1&y=2") == "http://example.com/a?x=1&y=2"

    assert normalize("http://example.com/#abc") == "http://example.com/#abc"
    assert normalize("http://example.com/a/b/c#abc") == "http://example.com/a/b/c#abc"
    assert normalize("http://example.com/a/b/c?x=1#abc") == "http://example.com/a/b/c?x=1#abc"

    assert normalize("http://example.com/a/./b/././c") == "http://example.com/a/b/c"
    assert normalize("http://example.com/a/../b") == "http://example.com/b"


def test_parse():
    assert parse("http://example.com") == ('http', 'example', 'com', '80', '/', '', '')
    assert parse("http://example.ac.at") == ('http', 'example', 'ac.at', '80', '/', '', '')
    assert parse("http://example.co.uk") == ('http', 'example', 'co.uk', '80', '/', '', '')

    assert parse("example.com") == ('', 'example', 'com', '', '', '', '')
    assert parse("example.com.") == ('', 'example', 'com', '', '', '', '')
    assert parse("example.ac.at") == ('', 'example', 'ac.at', '', '', '', '')
    assert parse("example.com/abc") == ('', 'example', 'com', '', '/abc', '', '')


def test_clean_netloc():
    assert _clean_netloc("example.com.") == "example.com"
    assert _clean_netloc("EXAMple.CoM") == "example.com"


#@pytest.mark.skipif("True")
def test_get_public_suffix_list():
    psl = _get_public_suffix_list()
    assert "de" in psl
    assert len(psl) > 6000
