#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from baiduSpider import BaiduSpider
from bilibiliSpider import BilibiliSpider
from wordcloud_generator import WordcloudGenerator
from xiguaSpider import XiguaSpider

class Controller(object):
    def __init__(self):
        self.baidu_spider = BaiduSpider()                   # 百度关键词爬虫
        self.bilibili_spider = BilibiliSpider()             # B站弹幕和评论爬虫
        self.xigua_spider = XiguaSpider()                   # 西瓜视频评论爬虫

        self.wordcloud_generator = WordcloudGenerator()     # 词云生成器

        # 创建需要的目录
        if not os.path.exists('./xml'): os.mkdir('./xml')

    # 获取各自的弹幕和评论的字符串列表，同时生成词云
    def launch(self, config):
        # 设置关键词
        baidu_keywords = ['留守青年', '新留守青年', '新农人', '返乡青年', '城市返乡']
        bilibili_keyword = '华农兄弟'

        # 爬行
        if config['bilibili']: self.crawl_bilibili(bilibili_keyword)      # Bilibili
        if config['baidu']: self.crawl_baidu(baidu_keywords)              # 百度
        if config['xigua']: self.crawl_xigua([bilibili_keyword])          # 西瓜

    def crawl_bilibili(self, kwd):
        print('- Bilibili -')
        bilibili_barrage_list, bilibili_comment_list = self.bilibili_spider.craw(kwd)
        barrages, IDs = zip(*bilibili_barrage_list)
        self.wordcloud_generator.generate_from_str(''.join(barrages), 'bilibili_barrage')
        self.wordcloud_generator.generate_from_str(''.join(bilibili_comment_list), 'bilibili_comment')

    def crawl_baidu(self, kwds):
        print('- 百度 -')
        for kwd in kwds:
            self.wordcloud_generator.generate_from_str(''.join(self.baidu_spider.craw(kwd)), 'baidu_title_'+kwd)

    def crawl_xigua(self, kwds):
        print('- 西瓜 -')
        for kwd in kwds:
            self.wordcloud_generator.generate_from_str(''.join(self.xigua_spider.get_comments_by_keyword(kwd)), 'xigua_comment')

# 各定义结束后，从这里开始实际处理
if __name__ == '__main__':
    Controller().launch({
        'baidu': False,
        'bilibili': False,
        'xigua': True
    })
