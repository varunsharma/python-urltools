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

import re
from urlparse import urlparse


PORT_RE = re.compile(r'(?<=.:)[1-9]+[0-9]{0,4}$')


def normalize(url):
    parts = urlparse(url)
    nurl = parts.scheme + '://'
    netloc = parts.netloc.rstrip('.').lower()
    port = "80"
    if PORT_RE.findall(netloc):
        netloc, port = netloc.split(":")
    nurl += netloc
    if port != "80":
        nurl += ":" + port
    if parts.path:
        nurl += parts.path
    else:
        nurl += '/'
    if parts.query:
        nurl += "?" + parts.query
    if parts.fragment:
        nurl += "#" + parts.fragment
    return nurl


def split(url):
    pass
