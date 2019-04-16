#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import urllib.request
import requests
from bs4 import BeautifulSoup
import re, json


class XiguaSpider(object):
    def __init__(self):
        self.headers = {
            'Host': 'www.ixigua.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.1547205979.1555327706; _gid=GA1.2.605476948.1555327706; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6680081574853281283'
        }
        self.proxy = {"http": '104.238.156.87:12724'}

    # 根据关键词获取所有评论
    def get_comments_by_keyword(self, keyword):
        total_comment_list = []
        id_list = self.getIdListByKeyword(keyword)
        for id in id_list:
            total_comment_list = total_comment_list + self.getCommentsByID(id)
        return total_comment_list


    # 根据关键词获得视频id列表
    def getIdListByKeyword(self, keyword):
        id_list = []

        #　解析关键词，转换为十六进制编码
        keyword_coded = urllib.request.quote(keyword)

        # 获取包含搜索结果的json数据
        url = 'https://www.ixigua.com/search_content/?format=json&autoload=true&count=10000&keyword=' + keyword_coded

        try:
            res = requests.get(url)
            #print(res.status_code)
            originStr = str(res.content, 'utf-8')
            findingRes = re.compile("\"id\": \d+").findall(originStr)

            # 提取ID
            for result in findingRes: id_list.append(result.split(' ')[1])
            print('获取到' + str(len(id_list)) + '个视频。')

            return id_list
        except requests.exceptions as e:
            print(e)
        except Exception as e:
            print(e)


    # 根据视频id获取评论列表
    def getCommentsByID(self, id):
        # 我也是这样觉得你好
        print('\n+=====================================\n视频：' + 'https://www.ixigua.com/a' + id)
        comment_list = []

        # 包含评论的json数据
        url = 'https://www.ixigua.com/api/comment/list/?group_id=' + id + '&item_id=' + id + '&offset=0&count=10000'
        print('评论内容url：' + url)

        # 初始json数据
        res = requests.get(url, headers=self.headers)
        originStr = str(res.content, encoding='utf-8')

        # 获取评论内容
        comments = json.loads(originStr)['data']['comments']
        for raw_comment in comments:
            raw_text = raw_comment['text']

            # 去掉emoji
            emojis = re.compile("<i.*?</span>").findall(raw_text)
            if emojis:
                for emoji in emojis:
                    raw_text = raw_text.replace(emoji, '')
            raw_text = re.sub('[，, 。, ！, 【, 】]', '', raw_text)
            comment_list.append(raw_text)
        print('本视频爬取评论' + str(len(comment_list)) + '条。')
        if comment_list: print(comment_list)
        return comment_list
