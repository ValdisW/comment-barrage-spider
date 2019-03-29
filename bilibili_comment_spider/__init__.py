#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import json

import jieba
from wordcloud import WordCloud

# 根据av字符串，获取评论列表
def get_comment_form_av(av):
    import time
    from selenium import webdriver

    comments_list = []
    original_url = 'https://www.bilibili.com/video/' + av
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(original_url)
    time.sleep(5)       # waiting for loading website
    driver.execute_script('var q=document.documentElement.scrollTop=100000')       # scroll downwards to load comments
    time.sleep(5)       # waiting for loading comments

    current_page = 1
    while True:
        # get comments from current page
        replyWraps = driver.find_elements_by_class_name("con")

        if len(replyWraps) == 0: break       # no comments
        else:
            print('\033[1;31;40m-第' + str(current_page) + '页-\033[0m')
            # 评论文本保存在list中
            for each in replyWraps:
                comment_text = each.find_element_by_class_name("text").text
                comments_list.append(comment_text)
                print('\033[1;33;40m【装填评论】\033[0m' + comment_text)

            # 【下一页】按钮
            try:
                next_button = driver.find_element_by_class_name("next")
            except Exception:
                print('最后一页啦')
                break

            if next_button:  # 还没有到最后一页
                current_page = current_page + 1
                next_button.click()

    return comments_list

get_comment_form_av('av43873105')


def colorFunc(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "rgb(0,0,0)"

class BilibiliCommentSpider(object):
    def __init__(self):
        self.headers = {
            'Host': 'www.bilibili.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'PSTM=1518190219; BD_UPN=12314753; BIDUPSID=39948ABD42E5CE87F6682DEBFFB8A76E; __cfduid=ddcfef2e028fcc58b8456290667600e8b1544282821; BDUSS=UZkbEcyei15T0ZJVX54QWd0Q1NabDBGc1E1b3ppZnNqZUl3Y3FIYm5Tb0hoMFJjQVFBQUFBJCQAAAAAAAAAAAEAAAAG67oed3IxOTk4MDYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf6HFwH-hxca; BAIDUID=7F7869C2438566745E00CA9C74C9943E:FG=1; ispeed_lsm=0; MCITY=-%3A; delPer=0; BD_CK_SAM=1; PSINO=3; BDRCVFR[pNjdDcNFITf]=mk3SLVN4HKm; H_PS_PSSID=1464_21110_28608_28584_28603_28626_28605; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=7db8Bvm68yV6m%2FHLrh3e7dX7rfnDT%2BeuxU9Hv7pftY3tvM%2BXoQyut74QRQQraXyg6osTdg'
        }

    def craw(self, keyword):
        print('Current keyword: %s' % keyword)
        keyword_coded = urllib.request.quote(keyword)
        page_index = 1

        a_list = []
        while True:
            print('Current page: %d' % page_index)
            url = 'https://www.baidu.com/s?wd=' + keyword_coded + '&pn=' + str(10 * (page_index - 1))
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            results = soup.select('h3 > a')  # a标签集合
            a_list = a_list + results

            page_index = page_index + 1

            has_next_page = re.search('下一页', str(res.content, encoding='utf-8'))
            if not has_next_page: break

        # 写入链接文件
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

        # 生成词云
        words = []
        for a in a_list: words.append(a.get_text())
        jb = ''.join(words)

        jb = ''.join(jb)
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


        print('计算词频...')
        freqs = wc.process_text(jb)
        print(freqs)

        print('生成json...')
        with open(keyword + '_freq.json', 'w', encoding='utf-8') as jsonf:
            json.dump(freqs, jsonf, ensure_ascii=False)

        print('生成词云...')
        wc.generate_from_frequencies(freqs)

        print('写入文件...')
        wc.to_file(keyword + '.jpg')