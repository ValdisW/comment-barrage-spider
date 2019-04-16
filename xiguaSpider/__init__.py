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

    # 根据关键词获得视频id列表
    def getIdListByKeyword(self, keyword):
        id_list = []

        #　解析关键词，转换为十六进制编码
        keyword_coded = urllib.request.quote(keyword)

        # 获取包含搜索结果的json数据
        url = 'https://www.ixigua.com/search_content/?format=json&autoload=true&count=10000&keyword=' + keyword_coded

        res = requests.get(url)
        originStr = str(res.content, 'utf-8')
        findingRes = re.compile("\"id\": \d+").findall(originStr)

        # 提取ID
        for result in findingRes: id_list.append(result.split(' ')[1])

        print(id_list)
        return id_list

    # 根据视频id获取评论
    def getCommentsByID(self, id):
        comment_list = []

        # 包含评论的json数据
        url = 'https://www.ixigua.com/api/comment/list/?group_id=' + id + '&item_id=' + id + '&offset=0&count=10000'

        # 初始文本数据
        res = requests.get(url, headers=self.headers)
        originStr = str(res.content, encoding='utf-8')

        # 获取评论内容
        comments = json.loads(originStr)['data']['comments']
        for raw_comment in comments:
            print(raw_comment['text'])
        '''
        if not replies_dic: break

        print('\033[1;31;40m-第' + str(page_num) + '页-\033[0m')
        for reply_dic in replies_dic:
            comment = reply_dic['content']['message']
            print('\033[1;33;40m【装填评论】\033[0m' + comment)
            comments_list.append(comment)

        # 提取text
        for result in findingRes: comment_list.append(result.split(' ')[1])

        print(comment_list)
        return comment_list
    '''

'''
        a_list = []
        while True:
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            results = soup.select('.r > a')  # a标签集合
            a_list = a_list + results

            page_index = page_index + 1

            has_next_page = re.search('下一页', str(res.content, encoding='utf-8'))
            if not has_next_page: break

        fh = open('./' + keyword + '.html', 'w')
        fh.write('<ol>')
        for a in a_list:
            try:
                fh.write('<li><a href=\'')
                fh.write(a.get('href'))
                fh.write('\'>')
                fh.write(a.get_text())
                fh.write('</a></li>')
            except Exception: continue
        fh.write('</ol>')
        fh.close()
'''


if __name__ == '__main__':
    keyword_list = ['华农兄弟']
    spider = XiguaSpider()
    for kwd in keyword_list: spider.getCommentsByID('6655959477348467211')
