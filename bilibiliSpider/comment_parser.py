#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
获取评论的模块。
'''

import time
import re

import urllib, requests, re, time, json
from bs4 import BeautifulSoup
from selenium import webdriver
import jieba
from wordcloud import WordCloud

# 根据av号获取弹幕
class Comment_parser(object):
    def __init__(self):
        pass

    # 根据关键词获取评论
    def get_comments_from_keyword(self, keyword):
        pass

    # 根据av字符串，获取评论列表
    '''
    def get_comments_from_av(self, av_str):
        comments_list = []
        original_url = 'https://www.bilibili.com/video/' + av_str
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get(original_url)
        time.sleep(5)  # waiting for loading website
        driver.execute_script('var q=document.documentElement.scrollTop=100000')  # scroll downwards to load comments
        time.sleep(5)  # waiting for loading comments

        current_page = 1
        while True:
            # get comments from current page
            replyWraps = driver.find_elements_by_class_name("con")

            if len(replyWraps) == 0:f\
                break  # no comments
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
    '''

    # 根据av获取评论列表
    def get_comments_from_av(self, av):
        comments_list = []

        # 获取av的数字部分
        aid = av[2:]

        # 本视频评论的总页数（或者是设置最大爬取页数）
        page_sum = 335
        '''
        video_url = 'https://www.bilibili.com/video/' + av_str + '/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.19'
        video_page_res = requests.get(video_url)
        fhandle = open('./bilibilipage.html', 'wb')
        fhandle.write(video_page_res.content)
        fhandle.close()
        '''

        # 循环爬取评论
        for page_num in range(1, page_sum + 1):
            comment_url = 'https://api.bilibili.com/x/v2/reply?&type=1&oid=' + aid + '&pn=' + str(page_num)
            res = requests.get(comment_url)
            ctt = str(res.content, encoding='utf-8')
            replies_dic = json.loads(ctt)['data']['replies']
            if not replies_dic: break

            print('\033[1;31;40m-第' + str(page_num) + '页-\033[0m')
            for reply_dic in replies_dic:
                comment = reply_dic['content']['message']
                print('\033[1;33;40m【装填评论】\033[0m' + comment)
                comments_list.append(comment)

        '''
        fh = open('./test.json', 'w', encoding='utf-8')
        fh.write(ctt)
        fh.close()
        '''
        print(av + ': 共获得' + str(len(comments_list)) + '条评论。')
        return comments_list


