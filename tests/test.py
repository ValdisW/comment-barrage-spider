#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os


if not os.path.exists('./wordcloud_imgs'): os.mkdir('./wordcloud_imgs')
fh = open('./wordcloud_imgs/23333.txt', 'w')
fh.write('233333333')
fh.close()