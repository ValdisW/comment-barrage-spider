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

        # 获取关键词对应的(av, 标题)列表
        av_and_title_list = self.get_av_from_keyword(keyword)

        # 逐个视频提取评论
        num_of_videos = len(av_and_title_list)
        video_index = 0
        for av_and_title in av_and_title_list:
            video_index += 1
            print('\n+=========================\n(' + str(video_index) + '/' + str(num_of_videos) + ')当前：处理' + av_and_title[0] + '：' + 'https://www.bilibili.com/video/' + av_and_title[0])
            print(av_and_title[1])
            comments = self.commentParser.get_comments_from_av(av_and_title[0])
            barrages = self.barrageParser.get_current_barrage_from_av(av_and_title[0])
            comment_list = comment_list + comments
            barrage_list = barrage_list + barrages
            print('+=========================')

        return barrage_list, comment_list

    # 历史模式，根据关键词和日期字符串获取某天的弹幕和评论信息（评论是最新的）
    def craw_history(self, keyword, dateStr):
        barrage_list = []

        # 获取关键词对应的(av, 标题)列表
        av_and_title_list = self.get_av_from_keyword(keyword)

        # 逐个视频提取评论
        num_of_videos = len(av_and_title_list)
        video_index = 0
        for av_and_title in av_and_title_list:
            video_index += 1
            print('\n+=========================\n(' + str(video_index) + '/' + str(num_of_videos) + ')当前：处理' + av_and_title[0] + '：' + 'https://www.bilibili.com/video/' + av_and_title[0])
            print(av_and_title[1])
            barrages = self.barrageParser.get_history_barrage_by_av(av_and_title[0], dateStr)
            barrage_list = barrage_list + barrages
            print('+=========================')

        return barrage_list
        # barrage_list = []
        # comment_list = []
        #
        # # 获取关键词对应的(av, 标题)列表
        # av_and_title_list = self.get_av_from_keyword(keyword)
        #
        # # 逐个视频提取评论
        # num_of_videos = len(av_and_title_list)
        # video_index = 0
        # for av_and_title in av_and_title_list:
        #     video_index += 1
        #     print('\n+=========================\n(' + str(video_index) + '/' + str(num_of_videos) + ')当前：处理' + av_and_title[0] + '：' + 'https://www.bilibili.com/video/' + av_and_title[0])
        #     print(av_and_title[1])
        #     comments = self.commentParser.get_comments_from_av(av_and_title[0])
        #     barrages = self.barrageParser.get_history_barrage_by_av(av_and_title[0], dateStr)
        #     comment_list = comment_list + comments
        #     barrage_list = barrage_list + barrages
        #     print('+=========================')
        #
        # return barrage_list, comment_list

    # 根据关键词，获取所有视频的av号
    def get_av_from_keyword(self, keyword):
        a_list = []  # 保存当前关键词对应的所有a标签
        av_list = []  # 保存当前关键词对应的所有视频的链接
        # 开始搜索
        print('开始搜索【' + keyword + '】...\n页码：', end='')
        for page in range(1, 51):  # page为页码
            print(str(page), end=' ')
            # 根据关键词和页码即可确定一个搜索页面
            current_url = 'https://search.bilibili.com/all?keyword=' + urllib.request.quote(keyword) + '&page=' + str(page)

            try:
                # 获取搜索界面(requests)
                res = requests.get(current_url, timeout=10)
                soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

                # 获取当前页面所有的视频a标签
                links = soup.find_all('a', class_='img-anchor')

                # 装填新的链接标签
                a_list = a_list + links
            except requests.exceptions as e:
                print(e)
            except Exception as e:
                print(e)
                print('超时了，下一个')

        print('\n' + '找到了' + str(len(a_list)) + '个视频。')

        # 遍历所有的a标签（包含地址、标题）
        for a in a_list:
            av_list.append((self.get_av_from_url(a['href']), a['title']))

        return av_list

    # 根据视频地址，获取av字符串(avxxxxxxxx)
    def get_av_from_url(self, bilibili_video_url):
        return re.search('av\d+', bilibili_video_url).group(0)
