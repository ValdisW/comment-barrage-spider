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

        video_index = 0
        for id in id_list:
            video_index += 1
            total_comment_list = total_comment_list + self.getCommentsByID(id)
        return total_comment_list


    # 根据关键词获得视频id列表
    def getIdListByKeyword(self, keyword):
        id_list = []

        #　解析关键词，转换为十六进制编码
        keyword_coded = urllib.request.quote(keyword)

        # 获取包含搜索结果的json数据
        url = 'https://www.ixigua.com/search_content/?format=json&autoload=true&count=10000&keyword=' + keyword_coded
        print('视频信息url：' + url)
        try:
            res = requests.get(url)
            #print(res.status_code)
            originStr = str(res.content, 'utf-8')
            print(originStr)
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
        print('\n+=====================================\n视频：' + 'https://www.ixigua.com/a' + id)
        comment_list = []

        raw_comments = []
        for offset in range(0, 10000, 20):
            # 包含评论的json地址
            url = 'https://www.ixigua.com/api/comment/list/?group_id=' + id + '&item_id=' + id + '&offset=' + str(offset) + '&count=20'

            # 获取并编码json数据
            res = requests.get(url, headers=self.headers)
            originStr = str(res.content, encoding='utf-8')

            # 获取评论内容
            new_raw_comments = json.loads(originStr)['data']['comments']
            if len(new_raw_comments) == 0: break

            # 收集
            raw_comments = raw_comments + new_raw_comments


        for raw_comment in raw_comments:
            raw_text = raw_comment['text']

            # 去掉emoji
            emojis = re.compile("<i.*?</span>").findall(raw_text)
            if emojis:
                for emoji in emojis:
                    raw_text = raw_text.replace(emoji, ' ')

            raw_text = re.sub('[，, 。, ！, 【, 】, 🔥, 😊]', ' ', raw_text)
            raw_text = re.sub('\s{2,}', ' ', raw_text)

            if re.search('龘鬞齾', raw_text): continue
            comment_list.append(raw_text)

        print('获取了' + str(len(comment_list)) + '条评论。')
        if comment_list: print(comment_list)
        print('+=====================================')

        return comment_list
