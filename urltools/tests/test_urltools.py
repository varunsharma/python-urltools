# -*- coding: utf-8 -*-
#import pytest

from urltools import parse, extract, encode, split, split_netloc, split_host
from urltools import normalize, normalize_path, normalize_query, unquote
from urltools.urltools import _get_public_suffix_list, _clean_netloc


#@pytest.mark.skipif("True")
def test_get_public_suffix_list():
    psl = _get_public_suffix_list()
    assert "de" in psl
    assert len(psl) > 6000


def test_normalize():
    assert normalize("") == ""
    assert normalize("http://example.com") == "http://example.com/"
    assert normalize("http://example.com/") == "http://example.com/"
    assert normalize("    http://example.com/      ") == "http://example.com/"
    assert normalize("https://example.com/") == "https://example.com/"
    assert normalize("hTTp://example.com/") == "http://example.com/"
    assert normalize("http://ExAMPLe.COM/") == "http://example.com/"
    assert normalize("http://example.com./") == "http://example.com/"
    assert normalize("http://example.com:/") == "http://example.com/"
    assert normalize("http://example.com/#") == "http://example.com/"

    # port
    assert normalize("http://example.com:80/") == "http://example.com/"
    assert normalize("https://example.com:443/") == "https://example.com/"
    assert normalize("ws://example.com:80/") == "ws://example.com/"
    assert normalize("http://example.com:8080/") == "http://example.com:8080/"

    # subdomain
    assert normalize("http://www.example.com/") == "http://www.example.com/"
    assert normalize("http://www.example.com") == "http://www.example.com/"
    assert normalize("http://foo.bar.example.com/") == "http://foo.bar.example.com/"

    # ip
    assert normalize("http://192.168.1.1/") == "http://192.168.1.1/"
    assert normalize("http://192.168.1.1:8088/foo?x=1") == "http://192.168.1.1:8088/foo?x=1"
    assert normalize("192.168.1.1") == "192.168.1.1"
    assert normalize("192.168.1.1:8080/foo/bar") == "192.168.1.1:8080/foo/bar"

    # path
    assert normalize("http://example.com/a") == "http://example.com/a"
    assert normalize("http://example.com/a/b/c") == "http://example.com/a/b/c"
    assert normalize("http://example.com/foo/") == "http://example.com/foo/"
    assert normalize("http://example.com/a/./b/././c") == "http://example.com/a/b/c"
    assert normalize("http://example.com/a/../b") == "http://example.com/b"
    assert normalize("http://example.com/./b") == "http://example.com/b"
    assert normalize("http://example.com/../b") == "http://example.com/b"
    assert normalize("http://example.com/////////foo") == "http://example.com/foo"
    assert normalize("http://example.com/foo/.../bar") == "http://example.com/foo/.../bar"
    assert normalize("http://example.com/foo+bar") == "http://example.com/foo+bar"
    assert normalize("http://example.com/.") == "http://example.com/"
    assert normalize("http://example.com/..") == "http://example.com/"
    assert normalize("http://example.com/./") == "http://example.com/"
    assert normalize("http://example.com/../") == "http://example.com/"
    assert normalize("http://example.com/a/..") == "http://example.com/"
    assert normalize("http://example.com/a/../") == "http://example.com/"

    # encoded path
    assert normalize("http://example.com/%25%32%35") == "http://example.com/%25"
    assert normalize("http://example.com/foo%25%32%35bar") == "http://example.com/foo%25bar"
    assert normalize("http://example.com/foo/%25%32%35/bar") == "http://example.com/foo/%25/bar"
    # %23 = #
    #assert normalize("http://example.com/foo%23bar") == "http://example.com/foo%23bar"

    # query
    assert normalize("http://example.com/?x=1") == "http://example.com/?x=1"
    assert normalize("http://example.com?x=1") == "http://example.com/?x=1"
    assert normalize("http://example.com/a?x=1") == "http://example.com/a?x=1"
    assert normalize("http://example.com/a/?x=1") == "http://example.com/a/?x=1"
    assert normalize("http://example.com/a?x=1&y=2") == "http://example.com/a?x=1&y=2"
    assert normalize("http://example.com/a?y=2&x=1") == "http://example.com/a?x=1&y=2"
    assert normalize("http://example.com/a?x=&y=2") == "http://example.com/a?y=2"

    # fragment
    assert normalize("http://example.com/#abc") == "http://example.com/#abc"
    assert normalize("http://example.com/a/b/c#abc") == "http://example.com/a/b/c#abc"
    assert normalize("http://example.com/a/b/c?x=1#abc") == "http://example.com/a/b/c?x=1#abc"

    # no scheme
    assert normalize("eXAmplE.com") == "example.com"
    assert normalize("example.com/a/../b") == "example.com/b"
    assert normalize("www.example.com") == "www.example.com"

    # username/password
    assert normalize("http://foo:bar@example.com") == "http://foo:bar@example.com/"
    assert normalize("http://Foo:BAR@exaMPLE.COM/") == "http://Foo:BAR@example.com/"

    # scheme without //
    assert normalize("mailto:foo@example.com") == "mailto:foo@example.com"
    assert normalize("mailto:foo@eXAMPle.cOM") == "mailto:foo@example.com"

    # malformed urls
    assert normalize("http://example.com/?foo") == "http://example.com/"
    assert normalize("http://example.com?foo") == "http://example.com/"
    assert normalize("http://example.com/foo//bar") == "http://example.com/foo/bar"
    assert normalize("http://example.com?") == "http://example.com/"
    assert normalize("http://example.com/?") == "http://example.com/"
    assert normalize("http://example.com//?") == "http://example.com/"
    assert normalize("http://example.com/foo/?http://example.com/bar/?x=http://examle.com/y/z") == "http://example.com/foo/?http://example.com/bar/?x=http://examle.com/y/z"
    assert normalize("http://example.com/#foo?bar") == "http://example.com/#foo?bar"
    assert normalize("http://example.com/#foo/bar/blub.html?x=1") == "http://example.com/#foo/bar/blub.html?x=1"
    assert normalize("http://example.com/foo#?=bar") == "http://example.com/foo#?=bar"
    assert normalize("http://example.com/foo/bar/http://example.com") == "http://example.com/foo/bar/http:/example.com"


def test_normalize_path():
    assert normalize_path("") == "/"
    assert normalize_path("/") == "/"
    assert normalize_path("/a") == "/a"
    assert normalize_path("a") == "a"
    assert normalize_path("/a/b") == "/a/b"
    assert normalize_path("/a/b/") == "/a/b/"
    assert normalize_path("/a/b/c") == "/a/b/c"
    assert normalize_path("/.") == "/"
    assert normalize_path("/..") == "/"
    assert normalize_path("/./") == "/"
    assert normalize_path("/../") == "/"
    assert normalize_path("/a/./b/././c") == "/a/b/c"
    assert normalize_path("/a/../b") == "/b"
    assert normalize_path("/a/b/../../c") == "/c"
    assert normalize_path("/////////foo") == "/foo"
    assert normalize_path("/foo/.../bar") == "/foo/.../bar"
    assert normalize_path("%25%32%35") == "%25"


def test_normalize_query():
    assert normalize_query("") == ""
    assert normalize_query("x=1&y=2") == "x=1&y=2"
    assert normalize_query("y=2&x=1") == "x=1&y=2"
    assert normalize_query("x=1&y=&z=3") == "x=1&z=3"
    assert normalize_query("x=&y=&z=") == ""
    assert normalize_query("=1&=2&=3") == ""


def test_unquote():
    pass


def test_encode():
    assert encode("http://exämple.com") == "http://xn--exmple-cua.com"
    assert encode("http://müller.de/") == "http://xn--mller-kva.de/"
    assert encode("http://ジェーピーニック.jp/") == "http://xn--hckqz9bzb1cyrb.jp/"
    assert encode("http://пример.рф") == "http://xn--e1afmkfd.xn--p1ai"
    assert encode("пример.рф") == "xn--e1afmkfd.xn--p1ai"


def test_parse():
    assert parse("http://example.com") == ('http', '', '', '', 'example', 'com', '', '', '', '')
    assert parse("http://example.com:8080") == ('http', '', '', '', 'example', 'com', '8080', '', '', '')
    assert parse("http://example.ac.at") == ('http', '', '', '', 'example', 'ac.at', '', '', '', '')
    assert parse("http://example.co.uk") == ('http', '', '', '', 'example', 'co.uk', '', '', '', '')
    assert parse("http://example.com/foo/") == ('http', '', '', '', 'example', 'com', '', '/foo/', '', '')
    assert parse("http://foo:bar@www.example.com:1234/foo/?x=1#bla") == ('http', 'foo', 'bar', 'www', 'example', 'com', '1234', '/foo/', 'x=1', 'bla')

    assert parse("example.com.") == ('', '', '', '', '', '', '', 'example.com.', '', '')
    assert parse("example.com/abc") == ('', '', '', '', '', '', '', 'example.com/abc', '', '')
    assert parse("www.example.com") == ('', '', '', '', '', '', '', 'www.example.com', '', '')

    assert parse("http://пример.рф") == ('http', '', '', '', 'пример', 'рф', '', '', '', '')
    assert parse("http://إختبار.مصر/") == ('http', '', '', '', 'إختبار', 'مصر', '', '/', '', '')

    assert parse("mailto:foo@bar.com") == ('mailto', 'foo', '', '', 'bar', 'com', '', '', '', '')


def test_extract():
    assert extract("http://example.com") == ('http', '', '', '', 'example', 'com', '', '', '', '')
    assert extract("http://example.com:8080") == ('http', '', '', '', 'example', 'com', '8080', '', '', '')
    assert extract("http://example.com:8080/abc?x=1&y=2#qwe") == ('http', '', '', '', 'example', 'com', '8080', '/abc', 'x=1&y=2', 'qwe')
    assert extract("http://example.ac.at") == ('http', '', '', '', 'example', 'ac.at', '', '', '', '')
    assert extract("http://example.co.uk/") == ('http', '', '', '', 'example', 'co.uk', '', '/', '', '')
    assert extract("http://foo.bar.example.co.uk") == ('http', '', '', 'foo.bar', 'example', 'co.uk', '', '', '', '')
    assert extract("http://foo:bar@www.example.com:1234/foo/?x=1#bla") == ('http', 'foo', 'bar', 'www', 'example', 'com', '1234', '/foo/', 'x=1', 'bla')

    assert extract("example.com.") == ('', '', '', '', 'example', 'com', '', '', '', '')
    assert extract("example.com/abc") == ('', '', '', '', 'example', 'com', '', '/abc', '', '')
    assert extract("www.example.com") == ('', '', '', 'www', 'example', 'com', '', '', '', '')
    assert extract("example.com/") == ('', '', '', '', 'example', 'com', '', '/', '', '')
    assert extract("example.com:8080") == ('', '', '', '', 'example', 'com', '8080', '', '', '')
    assert extract("example.com:8080/") == ('', '', '', '', 'example', 'com', '8080', '/', '', '')
    assert extract("example.com:8080/abc") == ('', '', '', '', 'example', 'com', '8080', '/abc', '', '')

    assert extract("http://пример.рф") == ('http', '', '', '', 'пример', 'рф', '', '', '', '')
    assert extract("http://إختبار.مصر/") == ('http', '', '', '', 'إختبار', 'مصر', '', '/', '', '')

    assert extract("mailto:foo@bar.com") == ('mailto', 'foo', '', '', 'bar', 'com', '', '', '', '')


def test_clean_netloc():
    assert _clean_netloc("example.com.") == "example.com"
    assert _clean_netloc("example.com:") == "example.com"
    assert _clean_netloc("EXAMple.CoM") == "example.com"
    assert _clean_netloc("fOO.baR.example.com") == "foo.bar.example.com"
    assert _clean_netloc("ПриМЕр.Рф") == "пример.рф"


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

    assert split("http://example.com?foo") == ('http', 'example.com', '', 'foo', '')
    assert split("http://example.com/?foo") == ('http', 'example.com', '/', 'foo', '')
    assert split("http://example.com?foo#bar") == ('http', 'example.com', '', 'foo', 'bar')
    assert split("http://example.com/#foo?bar") == ('http', 'example.com', '/', '', 'foo?bar')

    assert split("http://192.168.1.1/") == ('http', '192.168.1.1', '/', '', '')
    assert split("http://192.168.1.1:8080/") == ('http', '192.168.1.1:8080', '/', '', '')
    assert split("192.168.1.1") == ('', '', '192.168.1.1', '', '')


def test_split_netloc():
    assert split_netloc("example") == ('', '', 'example', '')

    assert split_netloc("example.com") == ('', '', 'example.com', '')
    assert split_netloc("www.example.com") == ('', '', 'www.example.com', '')

    assert split_netloc("example.com:80") == ('', '', 'example.com', '80')
    assert split_netloc("example.com:8080") == ('', '', 'example.com', '8080')
    assert split_netloc("foo.bar.example.com:8888") == ('', '', 'foo.bar.example.com', '8888')

    assert split_netloc("foo:bar@www.example.com:8080") == ('foo', 'bar', 'www.example.com', '8080')

    assert split_netloc("192.168.1.1") == ('', '', '192.168.1.1', '')
    assert split_netloc("192.168.1.1:8080") == ('', '', '192.168.1.1', '8080')


def test_split_host():
    assert split_host("example.com") == ('', 'example', 'com')
    assert split_host("www.example.com") == ('www', 'example', 'com')
    assert split_host("www.foo.bar.example.com") == ('www.foo.bar', 'example', 'com')
    assert split_host("example.ac.at") == ('', 'example', 'ac.at')

    assert split_host("example.jp") == ('', 'example', 'jp')
    assert split_host("foo.kyoto.jp") == ('', 'foo', 'kyoto.jp')

    assert split_host("example.gs.aa.no") == ('', 'example', 'gs.aa.no')

    assert split_host("例子.中国") == ('', '例子', '中国')
    assert split_host("உதாரணம்.இந்தியா") == ('', 'உதாரணம்', 'இந்தியா')
