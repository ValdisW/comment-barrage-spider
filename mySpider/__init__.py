#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from wordcloud import WordCloud

from mySpider import target_URL_manager, HTML_downloader, HTML_parser, outputer, barrage_parser
import urllib.request

def colorFunc(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "rgb(0,0,0)"

class Spider(object):
    def __init__(self):
        self.current_URL = ''
        self.target_URL = target_URL_manager.targetURLManager()
        self.HTML_downloader = HTML_downloader.HTMLDownloader()
        self.HTML_parser = HTML_parser.HTMLParser()
        self.HTML_outputer = outputer.Outputer()
        self.barrager_xml_parser = barrage_parser.Barrage_parser()
        self.av_list = []       # 保存所有相关视频的av号
        self.barrage_p_list = []

    def craw(self, keyword):
        # 获取所有相关视频的av号
        root_url = 'https://search.bilibili.com/all?keyword=' + urllib.request.quote(keyword) + '&from_source=banner_search&order=dm&duration=0&tids_1=0&single_column=0&page='

        # 初始页码
        page_num = 1

        # 初始URL
        self.current_URL = root_url + str(page_num)

        # 逐个搜索页面
        while True:
            print('Curent page:', page_num)
            # download，获取整个搜索页面的HTML文本str
            page = self.HTML_downloader.download(self.current_URL)

            # parse
            target_urls = self.HTML_parser.parse(self.current_URL, page)

            self.target_URL.add_URLs(target_urls)

            # if not self.HTML_parser.has_next_page:break
            if page_num >= 50: break

            # 更新URL
            page_num = page_num + 1
            self.current_URL = root_url + str(page_num)

        # 逐个视频进行弹幕爬取
        self.av_list = self.HTML_outputer.output(self.target_URL.target_URLs)
        video_index = 1
        for av_id in self.av_list:      # 访问所有视频
            print('处理av'+str(av_id)+'...('+str(video_index) + '/'+str(len(self.av_list))+')')
            #barrages_p_list = self.barrager_xml_parser.get_history_barrage_by_av(av_id)
            barrages_p_list = self.barrager_xml_parser.get_current_barrage_by_av(av_id)
            self.barrage_p_list = self.barrage_p_list + barrages_p_list
            print('已爬取弹幕数: %d' % len(self.barrage_p_list))
            video_index = video_index + 1

        # 保存弹幕
        barrage_text_list = []
        fhandle = open('./all_barrages.html', 'w')
        fhandle.write('<!doctype html><html><head><title>Barrages</title><style>*{margin: 0; padding: 0} li{font-size: 12px}</style></head><body><ol>')
        for barrage_p in self.barrage_p_list:
            barrage_text_list.append(barrage_p[0])
            fhandle.write('<li>')

            try: fhandle.write(str(barrage_p[0]))
            except Exception as e: continue

            fhandle.write('</li>')

        fhandle.write('</ol></body></html>')
        fhandle.close()

        # 生成词云
        all_barrages = ''.join(barrage_text_list)
        wc = WordCloud(
            font_path='./fonts/msyh.ttc',
            background_color='white',
            width=4961,
            height=3508,
            max_words=1000,
            color_func=colorFunc
        )
        print('计算词频...')
        freqs = wc.process_text(all_barrages)
        print(freqs)

        print('生成json...')
        with open('bilibili_barrages_freq.json', 'w', encoding='utf-8') as jsonf:
            json.dump(freqs, jsonf, ensure_ascii=False)

        print('生成词云...')
        wc.generate_from_frequencies(freqs)

        print('写入文件...')
        wc.to_file('bilibili_barrages_freq.jpg')


if __name__ == '__main__':
    print('Bilibili弹幕爬取...')

    Spider().craw('华农兄弟')