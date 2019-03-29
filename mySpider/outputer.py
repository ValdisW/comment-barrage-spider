#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import re


class Outputer(object):
    # datas为目标链接列表
    def output(self, datas):
        av_list = []

        # File operation
        fhandle = open('./output.html', 'w')
        fhandle.write('<html><body><ol>')

        for data in datas:
            fhandle.write('<li><a href=\'')
            fhandle.write(data)
            fhandle.write('\'>')

            result = re.search('av\d+', data)
            av_str = result.group(0)
            fhandle.write(av_str)

            av_num = int(av_str[2:])
            av_list.append(av_num)


            fhandle.write('</a></li>')

        fhandle.write('</ol></body></html>')
        fhandle.close()

        return av_list

