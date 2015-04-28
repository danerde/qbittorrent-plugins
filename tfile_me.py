#VERSION: 1.00
#AUTHORS: Boris Nagaev (bnagaev@gmail.com), Dan Erusalimchik (danerde@gmail.com)
# This plugin is licensed under the GNU GPL Version 2.

from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import re
from urllib import quote

hit_pattern = re.compile(r'''\s*<a href="(?P<desc_link>.+)">(?P<name>.+)</a>\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*<a href="(?P<link>.+)">(?P<size>.+)</a>\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*<b class="sd">(?P<seeds>.*)</b>\s*
\s*</td>\s*
\s*<td class="dl">\s*
\s*<b class="lc">(?P<leech>.+)</b>\s*''')
tag = re.compile(r'<.*?>')

class tfile_me(object):
    url = 'http://tfile.me';
    name = 'tfile.me'
    supported_categories = {'all': 0,
                            'movies': 37,
                            'tv': 1068,
                            'music': 67,
                            'games': 98,
                            'anime': 175,
                            'software': 118,
                            'pictures': 1075,
                            'books': 195}
    query_pattern = '%(url)s/forum/ssearch.php?q=%(q)s&c=%(f)i&start=%(start)i&o=newest&to=1&io=1'
    def __init__(self):
        pass
    def search_page(self, what, cat, start):
        params = {}
        params['url'] = self.url
        params['q'] = quote(what.decode('utf-8').encode('cp1251'))
        params['f'] = self.supported_categories[cat]
        params['start'] = start
        print self.query_pattern % params
        dat = retrieve_url(self.query_pattern % params)
        for hit in hit_pattern.finditer(dat):
            d = hit.groupdict()
            d['desc_link'] = self.url + d['desc_link']
            d['link'] = self.url + d['link']
            d['engine_url'] = self.url
            d['name'] = tag.sub('', d['name'])
            yield d


    def search(self, what, cat='all'):
        start = 0
        while True:
            ds = list(self.search_page(what, cat, start))
            if not ds:
                break
            for d in ds:
                prettyPrinter(d)
            start += 25

