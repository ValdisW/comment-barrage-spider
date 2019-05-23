#!/usr/bin/env python 
# -*- coding:utf-8 -*-
a = '\xe8\xb4\xa6\xe5\x8f\xb7\xe6\x9c\xaa\xe7\x99\xbb\xe5\xbd\x95'

ss = a.encode('raw_unicode_escape')
print(ss)
sss = ss.decode()
print(sss)