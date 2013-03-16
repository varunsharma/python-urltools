import pytest

from urltools import normalize, parse, _get_public_suffix_list


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


def test_parse():
    parts = parse("http://example.com")
    assert parts.scheme == "http"
    assert parts.domain == "example"
    assert parts.tld == "com"

    parts = parse("http://example.ac.at")
    assert parts.domain == "example"
    assert parts.tld == "ac.at"

    parts = parse("http://example.co.uk")
    assert parts.domain == "example"
    assert parts.tld == "co.uk"


#@pytest.mark.skipif("True")
def test_get_public_suffix_list():
    psl = _get_public_suffix_list()
    assert psl.get("de") != None
    assert len(psl) > 6000
