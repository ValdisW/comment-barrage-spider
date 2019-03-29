#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib.parse

class HTMLParser(object):
    def __init__(self):
        self.has_next_page = False

    def parse(self, url, page):
        if page is None or url is None: return
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(url, soup)

        #self.has_next_page = bool(soup.find('li', class_='next'))

        return new_urls

    def _get_new_urls(self, url, soup):
        new_urls = set()
        links = soup.find_all('a', class_='img-anchor')
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(url, new_url)

            new_urls.add(new_full_url)

        return new_urls
