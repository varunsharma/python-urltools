"""
Copyright (c) 2013 Roderick Baier

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import re
import urllib
from urlparse import unquote
from collections import namedtuple
from posixpath import normpath


__all__ = ["ParseResult", "SplitResult", "parse", "extract", "split",
           "split_netloc", "split_host", "assemble", "encode", "normalize",
           "normalize_path", "normalize_query"]


PSL_URL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'

def _get_public_suffix_list():
    """Get the public suffix list.
    """
    local_psl = os.environ.get('PUBLIC_SUFFIX_LIST')
    if local_psl:
        psl_raw = open(local_psl).readlines()
    else:
        psl_raw = urllib.urlopen(PSL_URL).readlines()
    psl = set()
    for line in psl_raw:
        item = line.strip()
        if item != '' and not item.startswith('//'):
            psl.add(item)
    return psl

PSL = _get_public_suffix_list()


SCHEMES = ['http', 'https', 'ftp', 'sftp', 'file', 'gopher', 'imap', 'mms',
           'news', 'nntp', 'telnet', 'prospero', 'rsync', 'rtsp', 'rtspu',
           'svn', 'git']
SCHEME_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
IP_CHARS = '0123456789.:'

SplitResult = namedtuple('SplitResult', ['scheme', 'netloc', 'path', 'query',
                                         'fragment'])
ParseResult = namedtuple('ParseResult', ['scheme', 'username', 'password',
                                         'subdomain', 'domain', 'tld', 'port',
                                         'path', 'query', 'fragment'])


def normalize(url):
    """Normalize a URL
    """
    url_parts = split(url.strip())
    if url_parts.scheme:
        netloc = url_parts.netloc
        path = url_parts.path
    else:
        netloc = url_parts.path
        path = ''
        if '/' in netloc:
            tmp = netloc.split('/', 1)
            netloc = tmp[0]
            path = '/' + tmp[1]
    username, password, host, port = split_netloc(netloc)
    parts = ParseResult(url_parts.scheme, username, password, None, host, None,
                        port, path, url_parts.query, url_parts.fragment)
    return assemble(parts, default_path='/')


def encode(url):
    """Encode URL
    """
    parts = extract(url)
    idna = lambda x: x.decode('utf-8').encode('idna')
    encoded = ParseResult(*(idna(p) for p in parts))
    return assemble(encoded)


def assemble(parts, default_path=''):
    """Assemble a URL from the result returned by extract() or parse()
    """
    nurl = ''
    if parts.scheme:
        if parts.scheme in SCHEMES:
            nurl += parts.scheme + '://'
        else:
            nurl += parts.scheme + ':'
    if parts.username and parts.password:
        nurl += parts.username + ':' + parts.password + '@'
    elif parts.username:
        nurl += parts.username + '@'
    if parts.subdomain:
        nurl += parts.subdomain + '.'
    nurl += parts.domain
    if parts.tld:
        nurl += '.' + parts.tld
    if parts.port and parts.port != '80':
        nurl += ':' + parts.port
    if parts.path:
        nurl += normalize_path(parts.path)
    elif parts.scheme in SCHEMES:
        nurl += default_path
    if parts.query:
        query = normalize_query(parts.query)
        if query:
            nurl += '?' + query
    if parts.fragment:
        nurl += '#' + parts.fragment
    return nurl


def normalize_path(path):
    """Normalize path (collapse etc.)
    """
    if path in ['//', '/', '']:
        return '/'
    return normpath(unquote(path))


def normalize_query(query):
    """Normalize query (sort params by name, remove params without value)
    """
    if query == '' or len(query) <= 2:
        return ''
    params = query.split('&')
    nparams = []
    for param in params:
        if '=' in param:
            k, v = param.split('=', 1)
            if k and v:
                nparams.append("%s=%s" % (k, v))
    nparams.sort()
    return '&'.join(nparams)


def parse(url):
    """Parse a URL
    """
    parts = split(url)
    if parts.scheme:
        netloc = parts.netloc
        (username, password, host, port) = split_netloc(netloc)
        (subdomain, domain, tld) = split_host(host)
    else:
        username = password = subdomain = domain = tld = port = ''
    return ParseResult(parts.scheme, username, password, subdomain, domain, tld,
                       port, parts.path, parts.query, parts.fragment)


def extract(url):
    """Extract as much information from a (relative) URL as possible
    """
    parts = split(url)
    if parts.scheme:
        netloc = parts.netloc
        path = parts.path
    else:
        netloc = parts.path
        path = ''
        if '/' in netloc:
            tmp = netloc.split('/', 1)
            netloc = tmp[0]
            path = '/' + tmp[1]
    (username, password, host, port) = split_netloc(netloc)
    (subdomain, domain, tld) = split_host(host)
    return ParseResult(parts.scheme, username, password, subdomain, domain, tld,
                       port, path, parts.query, parts.fragment)


def split(url):
    """Split URL into scheme, netloc, path, query and fragment
    """
    scheme = netloc = path = query = fragment = ''
    scheme_end = url.find(':')
    if scheme_end > 0:
        for c in url[:scheme_end]:
            if c not in SCHEME_CHARS:
                break
        else:
            scheme = url[:scheme_end].lower()
            rest = url[scheme_end:].lstrip(':/')
    if not scheme:
        rest = url
    l_path = rest.find('/')
    l_query = rest.find('?')
    l_frag = rest.find('#')
    if l_path > 0:
        netloc = rest[:l_path]
        if l_query > 0 and l_frag > 0:
            path = rest[l_path:min(l_query, l_frag)]
        elif l_query > 0:
            path = rest[l_path:l_query]
        elif l_frag > 0:
            path = rest[l_path:l_frag]
        else:
            path = rest[l_path:]
    else:
        if l_query > 0:
            netloc = rest[:l_query]
        elif l_frag > 0:
            netloc = rest[:l_frag]
        else:
            netloc = rest
    if l_query > 0:
        if l_frag > 0:
            query = rest[l_query+1:l_frag]
        else:
            query = rest[l_query+1:]
    if l_frag > 0:
        fragment = rest[l_frag+1:]
    if not scheme:
        path = netloc + path
        netloc = ''
    return SplitResult(scheme, netloc, path, query, fragment)


def _clean_netloc(netloc):
    """Remove trailing '.'s and ':'s from a URL and tolower
    """
    return netloc.rstrip('.:').decode('utf-8').lower().encode('utf-8')


def split_netloc(netloc):
    """Split netloc into username, password, host and port
    """
    username = password = host = port = ''
    if '@' in netloc:
        user_pw, netloc = netloc.split('@', 1)
        if ':' in user_pw:
            username, password = user_pw.split(':', 1)
        else:
            username = user_pw
    netloc = _clean_netloc(netloc)
    if '.' not in netloc:
        return username, password, netloc, ''
    if ':' in netloc:
        host, port = netloc.split(':')
    else:
        host = netloc
    return username, password, host, port


def split_host(host):
    """Use the Public Suffix List to split host into subdomain, domain and tld
    """
    domain = subdomain = tld = ''
    for c in host:
        if c not in IP_CHARS:
            break
    else:
        return '', host, ''
    parts = host.split('.')
    for i in range(len(parts)):
        tld = '.'.join(parts[i:])
        wildcard_tld = '*.' + tld
        exception_tld = '!' + tld
        if tld in PSL:
            domain = '.'.join(parts[:i])
            break
        if wildcard_tld in PSL:
            domain = '.'.join(parts[:i-1])
            tld = '.'.join(parts[i-1:])
            break
        if exception_tld in PSL:
            domain = '.'.join(parts[:i-1])
            tld = '.'.join(parts[i-1:])
            break
    if '.' in domain:
        (subdomain, domain) = domain.rsplit('.', 1) 
    return subdomain, domain, tld
