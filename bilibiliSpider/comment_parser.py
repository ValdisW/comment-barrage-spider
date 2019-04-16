#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
获取评论的模块。
'''

import requests, json

# 根据av号获取弹幕
class Comment_parser(object):

    # 根据av获取评论列表
    def get_comments_from_av(self, av):
        comments_list = []

        # 获取av的数字部分
        aid = av[2:]

        # 本视频评论的总页数（或者是设置最大爬取页数）
        page_sum = 1335

        # 循环爬取评论
        print('收集评论中...')
        for page_num in range(1, page_sum + 1):
            # 构建评论页的url
            comment_url = 'https://api.bilibili.com/x/v2/reply?&type=1&oid=' + aid + '&pn=' + str(page_num)

            try:
                # 获得json原始数据
                res = requests.get(comment_url)
                ctt = str(res.content, encoding='utf-8')

                # 解析json
                replies_dic = json.loads(ctt)['data']['replies']
                if not replies_dic: break

                print('\033[1;31;40m-第' + str(page_num) + '页-\033[0m', end=' ')
                for reply_dic in replies_dic:
                    comment = reply_dic['content']['message']
                    #print('\033[1;33;40m【装填评论】\033[0m' + comment)
                    comments_list.append(comment)
            except requests.exceptions as e:
                print(e)

        print('\n' + av + ': 共获得' + str(len(comments_list)) + '条评论。')
        return comments_list
