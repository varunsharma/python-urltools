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
from urlparse import urlparse


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


def normalize(url):
    parts = extract(url)
    nurl = parts.scheme + '://' if parts.scheme else ''
    nurl += parts.subdomain + '.' if parts.subdomain else ''
    nurl += parts.domain
    nurl += "." + parts.tld
    if parts.port and parts.port != '80':
        nurl += ':' + parts.port
    nurl += normpath(parts.path) if parts.path else ''
    if parts.query:
        nurl += '?' + parts.query
    if parts.fragment:
        nurl += '#' + parts.fragment
    return nurl


PORT_RE = re.compile(r'(?<=.:)[1-9]+[0-9]{0,4}$')
Result = namedtuple('Result', 'scheme subdomain domain tld port path query fragment')

def _clean_netloc(netloc):
    return netloc.rstrip('.').decode('utf-8').lower().encode('utf-8')

def _split_netloc(netloc):
    netloc = _clean_netloc(netloc)
    subdomain = ''
    domain = netloc
    tld = ''
    port = ''
    if PORT_RE.findall(netloc):
        domain, port = netloc.split(':')
    d = domain.split('.')
    for i in range(len(d)):
        tld = '.'.join(d[i:])
        wildcard_tld = '*.' + tld
        exception_tld = '!' + tld
        if tld in PSL:
            domain = '.'.join(d[:i])
            break
        if wildcard_tld in PSL:
            domain = '.'.join(d[:i-1])
            tld = '.'.join(d[i-1:])
            break
        if exception_tld in PSL:
            domain = '.'.join(d[:i-1])
            tld = '.'.join(d[i-1:])
            break
    if domain.find('.') > 0:
        print domain
        (subdomain, domain) = domain.rsplit('.', 1) 
    return subdomain, domain, tld, port

def parse(url):
    parts = urlparse(url)
    if parts.scheme:
        netloc = parts.netloc
        (subdomain, domain, tld, port) = _split_netloc(netloc)
    else:
        subdomain = domain = tld = port = ''
    path = parts.path if parts.path else '/'
    return Result(parts.scheme, subdomain, domain, tld, port, path, parts.query, parts.fragment)

def extract(url):
    parts = urlparse(url)
    if parts.scheme:
        netloc = parts.netloc
        path = parts.path if parts.path else '/'
    else:
        netloc = parts.path
        path = ''
        if netloc.find('/') > 0:
            res = netloc.split('/', 1)
            netloc = res[0]
            path = '/' + res[1]
    (subdomain, domain, tld, port) = _split_netloc(netloc)
    return Result(parts.scheme, subdomain, domain, tld, port, path, parts.query, parts.fragment)
