#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time

from wordcloud import WordCloud

def colorFunc(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "rgb(0,0,0)"

class WordcloudGenerator(object):
    def __init__(self):
        pass

    # 由字符串生成词云
    def generate_from_str(self, text_str, output_name):
        now = time.strftime('%Y-%m-%d', time.localtime())
        #text_str = ''.join(text_list)

        # 分词操作
        #text_str = jieba.cut(text_str)
        #text_str = ''.join(text_str)

        wc = WordCloud(
            font_path='./fonts/msyh.ttc',
            background_color='white',
            width=4961,     # A3
            height=3508,
            max_words=1000,
            color_func=colorFunc
        )
        print('计算词频...')
        freqs = wc.process_text(text_str)
        print(freqs)

        print('生成json...')
        with open(output_name + '_' + now + '.json', 'w', encoding='utf-8') as jsonf:
            json.dump(freqs, jsonf, ensure_ascii=False)

        print('生成词云...')
        wc.generate_from_frequencies(freqs)

        print('写入文件...')
        wc.to_file(output_name + '_' + now + '.jpg')