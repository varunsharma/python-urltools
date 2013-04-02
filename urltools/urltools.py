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
from collections import namedtuple
from posixpath import normpath


PSL_URL = 'http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1'

def _get_public_suffix_list():
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


SCHEMES = ['http', 'https', 'ftp']

def normalize(url):
    parts = extract(url)
    nurl = ''
    if parts.scheme:
        if parts.scheme in SCHEMES:
            nurl += parts.scheme + '://'
        else:
            nurl += parts.scheme + ':'
    if parts.username and parts.password:
        nurl += parts.username + ':' + parts.password + '@'
    nurl += parts.subdomain + '.' if parts.subdomain else ''
    nurl += parts.domain
    nurl += '.' + parts.tld
    if parts.port and parts.port != '80':
        nurl += ':' + parts.port
    if parts.path:
        nurl += normpath(parts.path)
    elif parts.scheme:
        if parts.scheme in SCHEMES:
            nurl += '/'
    if parts.query:
        nurl += '?' + parts.query
    if parts.fragment:
        nurl += '#' + parts.fragment
    return nurl


PORT_RE = re.compile(r'(?<=.:)[1-9]+[0-9]{0,4}$')
SCHEME_RE = re.compile(r'^[a-zA-Z]+:(//)?')
USER_RE = re.compile(r'^[^:@]*:[^:@]*@.*$')
SplitResult = namedtuple('SplitResult', 'scheme netloc path query fragment')
ParseResult = namedtuple('ParseResult', 'scheme username password subdomain domain tld port path query fragment')

def split(url):
    """Split URLs into scheme, netloc, path, query and fragment
    """
    scheme = netloc = path = query = fragment = ''
    if SCHEME_RE.findall(url):
        l = url.find(':')
        scheme = url[:l].lower()
        rest = url[l:].lstrip(':/')
    else:
        rest = url
    l_path = rest.find('/')
    l_query = rest.find('?')
    l_frag = rest.find('#')
    if l_path > 0:
        netloc = rest[:l_path]
        if l_query > 0:
            path = rest[l_path:l_query]
        elif l_frag > 0:
            path = rest[l_path:l_frag]
        else:
            path = rest[l_path:]
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
    return netloc.rstrip('.:').decode('utf-8').lower().encode('utf-8')

def _split_netloc(netloc):
    username = password = subdomain = tld = port = ''
    if USER_RE.findall(netloc):
        user_pw, netloc = netloc.split('@', 1)
        username, password = user_pw.split(':', 1)
    netloc = _clean_netloc(netloc)
    if netloc.find('.') == -1:
        return '', '', '', netloc, '', ''
    if PORT_RE.findall(netloc):
        domain, port = netloc.split(':')
    else:
        domain = netloc
    parts = domain.split('.')
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
    if domain.find('.') > 0:
        (subdomain, domain) = domain.rsplit('.', 1) 
    return username, password, subdomain, domain, tld, port

def parse(url):
    parts = split(url)
    if parts.scheme:
        netloc = parts.netloc
        (username, password, subdomain, domain, tld, port) = _split_netloc(netloc)
    else:
        username = password = subdomain = domain = tld = port = ''
    path = parts.path if parts.path else ''
    return ParseResult(parts.scheme, username, password, subdomain, domain, tld,
                       port, path, parts.query, parts.fragment)

def extract(url):
    parts = split(url)
    if parts.scheme:
        netloc = parts.netloc
        path = parts.path if parts.path else ''
    else:
        netloc = parts.path
        path = ''
        if netloc.find('/') > 0:
            tmp = netloc.split('/', 1)
            netloc = tmp[0]
            path = '/' + tmp[1]
    (username, password, subdomain, domain, tld, port) = _split_netloc(netloc)
    return ParseResult(parts.scheme, username, password, subdomain, domain, tld,
                       port, path, parts.query, parts.fragment)
