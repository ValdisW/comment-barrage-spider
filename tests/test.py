#!/usr/bin/env python 
# -*- coding:utf-8 -*-

fh = open('./下载.json', 'r')
a = fh.read().encode('utf-8').decode('unicode_escape')

fh1 = open('new.json', 'w')
fh1.write(a)