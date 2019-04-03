#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib

import requests
from bs4 import BeautifulSoup

from bilibiliSpider import barrage_parser, comment_parser
import re

# 爬取视频弹幕和评论
class BilibiliSpider(object):
    def __init__(self):
        self.barrageParser = barrage_parser.Barrage_parser()    # 弹幕解析器
        self.commentParser = comment_parser.Comment_parser()    # 评论解析器

    # 实际爬取，根据关键词获取弹幕列表和评论列表
    def craw(self, keyword):
        barrage_list = []
        comment_list = []

        # 获取关键词对应的av列表
        av_list = self.get_av_from_keyword(keyword)

        # 逐个视频提取评论
        for av in av_list:
            comments = self.commentParser.get_comments_from_av(av)
            barrages = self.barrageParser.get_current_barrage_from_av(av)
            comment_list = comment_list + comments
            barrage_list = barrage_list + barrages

        return barrage_list, comment_list

    # 根据关键词，获取所有视频的av号
    def get_av_from_keyword(self, keyword):
        a_list = []  # 保存当前关键词对应的所有a标签
        av_list = []  # 保存当前关键词对应的所有视频的链接
        # 开始搜索
        print('获取视频...')
        for page in range(1, 51):  # page为页码
            print('当前第' + str(page) + '页')
            # 根据关键词和页码即可确定一个搜索页面
            current_url = 'https://search.bilibili.com/all?keyword=' + urllib.request.quote(keyword) + '&page=' + str(page)

            # 获取搜索界面(requests)，分析内容，提取av号(beautifulsoup)
            res = requests.get(current_url)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            # 获取当前页面所有的视频a标签
            links = soup.find_all('a', class_='img-anchor')

            # 装填新的链接标签
            a_list = a_list + links
        print('共找到了' + str(len(a_list)) + '个视频。')

        # 遍历所有的a标签
        for a in a_list:
            av_list.append(self.get_av_from_url(a['href']))

        return av_list

    # 根据视频地址，获取av字符串(avxxxxxxxx)
    def get_av_from_url(self, bilibili_video_url):
        return re.search('av\d+', bilibili_video_url).group(0)
