#!/usr/bin/env python
# -*- coding:utf-8 -*-

from baiduSpider import BaiduSpider
from bilibiliSpider import BilibiliSpider
from wordcloud_generator import WordcloudGenerator

class Controller(object):
    def __init__(self):
        self.baidu_spider = BaiduSpider()                   # 百度关键词爬虫
        self.bilibili_spider = BilibiliSpider()             # B站弹幕和评论爬虫

        self.wordcloud_generator = WordcloudGenerator()     # 词云生成器

    def launch(self):
        # 设置爬取关键词
        baidu_keywords = ['留守青年', '新留守青年', '新农人', '返乡青年', '城市返乡']
        bilibili_keyword = '华农兄弟'

        baidu_titles_list = []

        # 开始爬行，获取各自的弹幕和评论的字符串列表，同时生成词云
        print('合成词云…')
        for kwd in baidu_keywords:
            self.wordcloud_generator.generate_from_str(''.join(self.baidu_spider.craw(kwd)))

        bilibili_barrage_list, bilibili_comment_list = self.bilibili_spider.craw(bilibili_keyword, 'bilibili_comment')
        self.wordcloud_generator.generate_from_str(''.join(bilibili_barrage_list), 'bilibili_barrage')
        self.wordcloud_generator.generate_from_str(''.join(bilibili_comment_list), 'bilibili_comment')

        print(baidu_titles_list)

if __name__ == '__main__':
    controller = Controller().launch()
