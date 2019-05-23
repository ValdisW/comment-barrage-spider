#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wordcloud_generator import WordcloudGenerator
import os

class JsonMerger(object):
    def __init__(self):
        pass

    # 把某个目录下所有百度的json文件按天合并。path文件夹目录
    def mergeBaiduJsonsByPath(self, path):
        baidu_files = []        # 保存目标目录下所有百度的json文件
        files = os.listdir(path)
        for file in files:
            if file[0:11] == 'baidu_title':
                baidu_files.append(file)

        dict = {}
        for file in baidu_files:
            dateStr = file[-15:-5]
            dict[dateStr] = []
        for file in baidu_files:
            dateStr = file[-15:-5]
            dict[dateStr].append(path + '/' + file)

        if not os.path.exists('./merged_jsons'): os.mkdir('./merged_jsons')
        for d in dict:
            if len(dict[d]) == 5:
                WordcloudGenerator.merge_jsons('./merged_jsons/baidu_' + d, dict[d])

    # 把某个目录下所有的bilibili的json文件按天合并。
    def mergeBilibiliJsonsByPath(self, path):
        bilibili_files = []        # 保存目标目录下所有bilibili的json文件
        files = os.listdir(path)
        for file in files:
            if file[0:8] == 'bilibili':
                bilibili_files.append(file)

        dict = {}
        for file in bilibili_files:
            dateStr = file[-15:-5]
            dict[dateStr] = []
        for file in bilibili_files:
            dateStr = file[-15:-5]
            dict[dateStr].append(path + '/' + file)

        if not os.path.exists('./merged_jsons_bilibili'): os.mkdir('./merged_jsons_bilibili')
        for d in dict:
            if len(dict[d]) == 2:
                print(dict[d])
                WordcloudGenerator.merge_jsons('./merged_jsons_bilibili/bilibili_' + d, dict[d])

    # 把某个目录下三个平台数据合成一个json文件
    def mergeAllJsonsByPath(self, path):
        files = os.listdir(path)
        '''
        for file in files:
            if file[0:5] == 'baidu':
                pass
                #print(file)
            if file[0:13] == 'xigua_comment':
                pass
                #print(file)
            print(file[0:20])
        '''

        dict = {}
        for file in files:
            dateStr = file[-15:-5]
            dict[dateStr] = []
        for file in files:
            dateStr = file[-15:-5]
            dict[dateStr].append(path + '/' + file)

        if not os.path.exists('./merged_jsons_all'): os.mkdir('./merged_jsons_all')
        for d in dict:
            if len(dict[d]) == 3:
                print(dict[d])
                WordcloudGenerator.merge_jsons('./merged_jsons_all/all_' + d, dict[d])

merger = JsonMerger()
merger.mergeAllJsonsByPath('./stages')