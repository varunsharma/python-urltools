# -*- coding: utf-8 -*-
#import pytest

from urltools import normalize, parse, extract
from urltools.urltools import _clean_netloc, _split_netloc
from urltools.urltools import _get_public_suffix_list, split


def test_normalize():
    assert normalize("http://example.com") == "http://example.com/"
    assert normalize("http://example.com/") == "http://example.com/"
    assert normalize("https://example.com/") == "https://example.com/"
    assert normalize("hTTp://example.com/") == "http://example.com/"
    assert normalize("http://ExAMPLe.COM/") == "http://example.com/"
    assert normalize("http://example.com./") == "http://example.com/"
    assert normalize("http://example.com:80/") == "http://example.com/"
    assert normalize("http://example.com:/") == "http://example.com/"
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

    assert normalize("eXAmplE.com") == "example.com"
    assert normalize("example.com/a/../b") == "example.com/b"

    assert normalize("http://www.example.com") == "http://www.example.com/"
    assert normalize("www.example.com") == "www.example.com"


def test_parse():
    assert parse("http://example.com") == ('http', '', 'example', 'com', '', '/', '', '')
    assert parse("http://example.com:8080") == ('http', '', 'example', 'com', '8080', '/', '', '')
    assert parse("http://example.ac.at") == ('http', '', 'example', 'ac.at', '', '/', '', '')
    assert parse("http://example.co.uk") == ('http', '', 'example', 'co.uk', '', '/', '', '')

    assert parse("example.com.") == ('', '', '', '', '', 'example.com.', '', '')
    assert parse("example.com/abc") == ('', '', '', '', '', 'example.com/abc', '', '')
    assert parse("www.example.com") == ('', '', '', '', '', 'www.example.com', '', '')

    assert parse("http://пример.рф") == ('http', '', 'пример', 'рф', '', '/', '', '')
    assert parse("http://إختبار.مصر/") == ('http', '', 'إختبار', 'مصر', '', '/', '', '')


def test_extract():
    assert extract("http://example.com") == ('http', '', 'example', 'com', '', '/', '', '')
    assert extract("http://example.com:8080") == ('http', '', 'example', 'com', '8080', '/', '', '')
    assert extract("http://example.com:8080/abc?x=1&y=2#qwe") == ('http', '', 'example', 'com', '8080', '/abc', 'x=1&y=2', 'qwe')
    assert extract("http://example.ac.at") == ('http', '', 'example', 'ac.at', '', '/', '', '')
    assert extract("http://example.co.uk") == ('http', '', 'example', 'co.uk', '', '/', '', '')
    assert extract("http://foo.bar.example.co.uk") == ('http', 'foo.bar', 'example', 'co.uk', '', '/', '', '')

    assert extract("example.com.") == ('', '', 'example', 'com', '', '', '', '')
    assert extract("example.com/abc") == ('', '', 'example', 'com', '', '/abc', '', '')
    assert extract("www.example.com") == ('', 'www', 'example', 'com', '', '', '', '')
    assert extract("example.com/") == ('', '', 'example', 'com', '', '/', '', '')
    assert extract("example.com:8080") == ('', '', 'example', 'com', '8080', '', '', '')
    assert extract("example.com:8080/") == ('', '', 'example', 'com', '8080', '/', '', '')
    assert extract("example.com:8080/abc") == ('', '', 'example', 'com', '8080', '/abc', '', '')

    assert extract("http://пример.рф") == ('http', '', 'пример', 'рф', '', '/', '', '')
    assert extract("http://إختبار.مصر/") == ('http', '', 'إختبار', 'مصر', '', '/', '', '')


def test_clean_netloc():
    assert _clean_netloc("example.com.") == "example.com"
    assert _clean_netloc("example.com:") == "example.com"
    assert _clean_netloc("EXAMple.CoM") == "example.com"
    assert _clean_netloc("fOO.baR.example.com") == "foo.bar.example.com"
    assert _clean_netloc("ПриМЕр.Рф") == "пример.рф"


def test_split_netloc():
    assert _split_netloc("example.com") == ('', 'example', 'com', '')
    assert _split_netloc("example.ac.at") == ('', 'example', 'ac.at', '')

    assert _split_netloc("example.jp") == ('', 'example', 'jp', '')
    assert _split_netloc("foo.kyoto.jp") == ('', 'foo', 'kyoto.jp', '')

    assert _split_netloc("example.gs.aa.no") == ('', 'example', 'gs.aa.no', '')

    assert _split_netloc("例子.中国") == ('', '例子', '中国', '')
    assert _split_netloc("உதாரணம்.இந்தியா") == ('', 'உதாரணம்', 'இந்தியா','')

    assert _split_netloc("example.com:80") == ('', 'example', 'com', '80')
    assert _split_netloc("example.com:8080") == ('', 'example', 'com', '8080')

    assert _split_netloc("www.example.com") == ('www', 'example', 'com', '')
    assert _split_netloc("foo.bar.example.com:8888") == ('foo.bar', 'example', 'com', '8888')

    assert _split_netloc("example") == ('', 'example', '', '')


#@pytest.mark.skipif("True")
def test_get_public_suffix_list():
    psl = _get_public_suffix_list()
    assert "de" in psl
    assert len(psl) > 6000


def test_split():
    assert split("http://www.example.com") == ('http', 'www.example.com', '', '', '')
    assert split("http://www.example.com/") == ('http', 'www.example.com', '/', '', '')
    assert split("http://www.example.com/abc") == ('http', 'www.example.com', '/abc', '', '')

    assert split("http://www.example.com:80") == ('http', 'www.example.com:80', '', '', '')
    assert split("http://www.example.com:8080") == ('http', 'www.example.com:8080', '', '', '')
    assert split("http://www.example.com:8080/abc") == ('http', 'www.example.com:8080', '/abc', '', '')

    assert split("http://www.example.com/?x=1") == ('http', 'www.example.com', '/', 'x=1', '')
    assert split("http://www.example.com/abc?x=1") == ('http', 'www.example.com', '/abc', 'x=1', '')
    assert split("http://www.example.com/abc?x=1&y=2") == ('http', 'www.example.com', '/abc', 'x=1&y=2', '')

    assert split("http://www.example.com/abc#foo") == ('http', 'www.example.com', '/abc', '', 'foo')
    assert split("http://www.example.com/abc?x=1&y=2#foo") == ('http', 'www.example.com', '/abc', 'x=1&y=2', 'foo')

    assert split("mailto:foo@bar.com") == ('mailto', 'foo@bar.com', '', '', '')

    assert split("example.com") == ('', '', 'example.com', '', '')
    assert split("example.com.") == ('', '', 'example.com.', '', '')
    assert split("www.example.com") == ('', '', 'www.example.com', '', '')
    assert split("www.example.com/abc") == ('', '', 'www.example.com/abc', '', '')
    assert split("www.example.com:8080") == ('', '', 'www.example.com:8080', '', '')
    assert split("www.example.com:8080/abc") == ('', '', 'www.example.com:8080/abc', '', '')

    assert split("foo/bar") == ('', '', 'foo/bar', '', '')
    assert split("/foo/bar") == ('', '', '/foo/bar', '', '')
