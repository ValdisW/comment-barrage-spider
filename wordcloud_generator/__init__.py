#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import os

from wordcloud import WordCloud

def colorFunc(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "rgb(0,0,0)"

#　词云生成以及词频简单处理的类
class WordcloudGenerator(object):
    # 由字符串生成词云
    @staticmethod
    def generate_from_str(text_str, output_name):
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

        print('生成词频json...')
        if not os.path.exists('./wordcloud_json'): os.mkdir('./wordcloud_json')
        with open('./wordcloud_json/' + output_name + '_' + now + '.json', 'w', encoding='utf-8') as jsonf:
            json.dump(freqs, jsonf, ensure_ascii=False)

        # 项目原因这里不再生成词云图
        #
        # print('生成词云...')
        # wc.generate_from_frequencies(freqs)
        #
        # print('写入文件...')
        # if not os.path.exists('./wordcloud_imgs'): os.mkdir('./wordcloud_imgs')
        # wc.to_file('./wordcloud_imgs/' + output_name + '_' + now + '.jpg')

    # 由词频生成词云
    @staticmethod
    def generate_from_freq(text_freq, output_name):
        now = time.strftime('%Y-%m-%d', time.localtime())   # 计算当前年月日
        wc = WordCloud(
            font_path='./fonts/msyh.ttc',
            background_color='white',
            prefer_horizontal=1,
            mode="RGBA",
            contour_width=0.5,
            relative_scaling=1,
            width=496,     # A3
            height=350,
            max_words=100,
            color_func=colorFunc
        )
        print('生成词云...')
        wc.generate_from_frequencies(text_freq)

        print('写入文件...')
        wc.to_file('./' + output_name + '_' + now + '.png')


    # 由json文件获取词频
    @staticmethod
    def get_freq_from_json(json_file):
        with open(json_file, 'r', encoding='utf-8') as jsonf:
            content = jsonf.read()
            freq_dict = json.loads(content)
        return freq_dict

    # 由json文件生成词云
    @staticmethod
    def generate_from_json(json_file):
        freq_dict = WordcloudGenerator.get_freq_from_json(json_file)
        print(freq_dict)
        WordcloudGenerator.generate_from_freq(freq_dict, '百度_测试')

    # 合并多个词频的json文件。接受json路径的数组
    @staticmethod
    def merge_jsons(newName, jsons):
        merged_json = {}
        for simple_json in jsons:
            merged_json.update(WordcloudGenerator.get_freq_from_json(simple_json))
        with open(newName + '.json', 'w', encoding='utf-8') as f:
            json.dump(merged_json, f, ensure_ascii=False)
        return merged_json

