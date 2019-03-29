#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import urllib.request
import requests
from bs4 import BeautifulSoup
import re


class Spider(object):
    def __init__(self):
        self.headers = {
            'Host': 'www.google.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'CGIC=IlV0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44; CONSENT=YES+CN.zh-CN+20170611-09-0; HSID=Awthj_7oy-FxeCzW8; SSID=ALidK0sdNCIu2UeHY; APISID=xou-bI6nFGCRBGTY/ALv-bC3hjyPV2Vgr2; SAPISID=XVXo_weO7nCG1KwH/Aq1wnuQpr1pinSGfp; SID=Zgan8xSJBszT5RQMzG6_9w3_H3EIaxsOJJ9nMgfXQLaUDHMd4gFKZi4Om1y7MCPxSNFo1w.; OTZ=4804459_24_24__24_; NID=179=oSfY6jypLqo9Ys1nsvr4VpHa2kTuMHlnr9NIfRE_DfqNU_l3Xr1T5h4fCCstY1Ba06qHpolt6wVrKxV-Cc59f3IfNwxYyV3h8ubwjsB0WDzALDVUlMJmbGyyzgmvsUR-sxHORnDm3gQNpP88YqGs3VS6HLoOafXnyttWu27nHUWVDxgpAgao4wJLXxUV1eUrd1jkzz5HlcKflL1aZtkdfyYkKjEo-h85c06C1nMPRqqvx_m90X9b9p32p7dJOf5s24Fyzwp1iQe3NWeGHEVQh3jjXRTHPe2YOrAl12W3M9BEbtmEBua_VXl9uBOPpEafYv3iz8ybh44iAeTwo5-2o4KDUdYWeMl5z-CyLOVF; 1P_JAR=2019-03-16-11; DV=8xBMq7KP0k1cEG9bxDlsaDO72sllmNbgED6dyQS6fQIAAHAE6YfMsZ7o6gAAAEBRffM1_geJTwAAAOa5uMWkZ8hqFQAAAA; SIDCC=AN0-TYv-0Onv3_wKJrsiypjppx-SPff28bDNaBG1SD2JkiGKu-RbHUoAMDpHG5jaV0xPVeEI36G3ttmxog; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTU1MjczNzQxMTU5ODAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MzE0Nzg2NDk4IGxvbmdpdHVkZV9lNzoxMjAyNjQ3Mzg5fSByYWRpdXM6MTg2MDA='
        }
        self.proxy = {"http": '104.238.156.87:12724'}

    def craw(self, keyword):
        print('Current keyword: %s' % keyword)
        keyword_coded = urllib.request.quote(keyword)
        page_index = 1

        a_list = []
        while True:
            print('Current page: %d' % page_index)
            url = 'https://www.google.com/search?q=' + keyword_coded + '&start=' + str(10 * (page_index - 1))
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            results = soup.select('.r > a')  # a标签集合
            a_list = a_list + results

            page_index = page_index + 1

            has_next_page = re.search('下一页', str(res.content, encoding='utf-8'))
            if not has_next_page: break

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



if __name__ == '__main__':
    keyword_list = ['留守青年', '新留守青年', '新农人', '返乡青年', '城市返乡']
    spider = Spider()
    for kwd in keyword_list: spider.craw(kwd)
