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
            'Host': 'www.sogou.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'dt_ssuid=947284168; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=5806043950; SUV=00D82B8778DD209F5B5926C19A14F874; SUID=412E88753118960A000000005BE1BD0D; IPLOC=CN3202; CXID=DE99CD746527BEF13CC9829B2C4C6234; ABTEST=1|1552799124|v17; browerV=3; osV=1; pgv_pvi=973217792; PHPSESSID=4rdfm8u58593n9imis3duiici5; SUIR=444AD0614640C2057F8BF87F46464BC7; sct=15; taspeed=taspeedexist; pgv_si=s3867962368; sst0=575; ld=Xlllllllll2t0NQ@lllllVh5ReolllllJJUGlyllllolllll9klll5@@@@@@@@@@; SNUID=0925DB6CB4B637E65C974D79B4DD48ED; seccodeRight=success; successCount=2|Mon, 18 Mar 2019 03:24:55 GMT'
        }


    def craw(self, keyword):
        print('Current keyword: %s' % keyword)
        keyword_coded = urllib.request.quote(keyword)
        page_index = 1

        a_list = []
        while True:
            print('Current page: %d' % page_index)
            url = 'https://www.sogou.com/web?query=' + keyword_coded + '&page=' + str(page_index)
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
        jb = ' '.join(jb)

        print(jb)

        wc = WordCloud(
            font_path='./fonts/msyh.ttc',
            background_color='white',
            width=4961,
            height=3508,
            max_words=100,
            color_func=colorFunc
        )

        wc.generate(jb)
        print('写入文件...')
        filename = keyword + '_sogou.jpg'
        wc.to_file(filename)

if __name__ == '__main__':
    keyword_list = ['留守青年', '新留守青年', '新农人', '返乡青年', '城市返乡']
    spider = Spider()
    for kwd in keyword_list: spider.craw(kwd)
