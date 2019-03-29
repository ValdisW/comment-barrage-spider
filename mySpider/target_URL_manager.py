#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class targetURLManager(object):
    def __init__(self):
        self.target_URLs = set()

    def add_URLs(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_URL(url)

    def add_URL(self, url):
        if url is None:
            return
        if url not in self.target_URLs:
            self.target_URLs.add(url)