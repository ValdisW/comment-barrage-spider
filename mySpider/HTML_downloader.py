#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import urllib.request


class HTMLDownloader(object):
    def download(self, url):

        if url is None: return None

        res = urllib.request.urlopen(url)
        if res.getcode() != 200: return None

        return str(res.read(), encoding='utf-8')