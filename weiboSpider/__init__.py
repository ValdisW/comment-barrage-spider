#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

import jieba
from wordcloud import WordCloud

def colorFunc(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "rgb(0,0,0)"

class Spider(object):
    def __init__(self):
        self.headers = {
            'Host': 's.weibo.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'SINAGLOBAL=511913791152.645.1508553196423; UM_distinctid=1677298777c6d3-078a8a44d43a44-6313363-144000-1677298777ee52; un=18861800510; SCF=AtpU8isEVW6dahkwsrKggMCVAk2rFx1LCD03ebthDu3CXlSwqSkDkxPYpumZic00atKRSxMERH3iVA6q1YICH6I.; SUHB=0KAxLLfRtWyixM; _s_tentry=-; Apache=7171390981957.64.1552833546758; ULV=1552833546765:180:12:1:7171390981957.64.1552833546758:1552700871003; webim_unReadCount=%7B%22time%22%3A1552907635529%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A3372%2C%22allcountNum%22%3A3372%2C%22msgbox%22%3A0%7D; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhLUvrVpDQl7NdASakLn-.W5JpVF02R1hqp1h57SK27; SUB=_2AkMr0_JMdcPxrABYnf4TyW_ga4RH-jyYBpu6An7uJhMyAxgv7nwWqSVutBF-XBcRRiUGbLjWoSWyWZE1xvsUhWji; login_sid_t=071573f76f89eb1fe1a56aecb807f4d3; cross_origin_proto=SSL; UOR=,,login.sina.com.cn; WBStorage=201903181949|undefined'
        }
        self.accounts = [
            {'username': 'rutawu383@163.com', 'password': 'XBEuoe124v3'},
            {'username': 'guojin0194@163.com', 'password': 'HKGrdb795V6'},
            {'username': 'yipi88238@163.com', 'password': 'CEQeoh059Xc'},
            {'username': 'bairis678208@163.com', 'password': 'JEKcql286UH'},
            {'username': 'jian34508@163.com', 'password': 'FBGtgc704h6'},
        ]

    def craw(self, keyword):
        print('Current keyword: %s' % keyword)
        keyword_coded = urllib.request.quote(keyword)
        #page_index = 1

        p_list = []
        for page_index in range(1, 51):
            print('Current page: %d' % page_index)
            url = 'https://s.weibo.com/weibo?q=' + keyword + '&scope=ori&suball=1&Refer=g&page=' + str(page_index)
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            results = soup.select('p.txt')  # p标签集合
            p_list = p_list + results
            print(p_list)

        # 写入p标签文件
        fh = open('./' + keyword + '.html', 'w')
        fh.write('<ol>')
        for p in p_list:
            try:
                fh.write('<li><p>')
                fh.write(p.get_text())
                fh.write('</p></li>')
            except Exception: continue
        fh.write('</ol>')
        fh.close()

        # 生成词云
        words = []
        for p in p_list: words.append(p.get_text())
        jb = ''.join(words)

        jb = ''.join(jb)
        jb = re.sub('O网页链接', '', jb)
        jb = re.sub('收起全文d', '', jb)
        jb = jieba.cut(jb)
        jb = ''.join(jb)

        print(jb)

        wc = WordCloud(
            font_path='./fonts/msyh.ttc',
            background_color='white',
            width=4961,
            height=3508,
            max_words=1000,
            color_func=colorFunc
        )

        wc.generate(jb)
        print('写入文件...')
        filename = keyword + '.jpg'
        wc.to_file(filename)

if __name__ == '__main__':
    keyword_list = ['留守青年', '新留守青年', '新农人', '返乡青年', '城市返乡']
    spider = Spider()
    for kwd in keyword_list: spider.craw(kwd)
