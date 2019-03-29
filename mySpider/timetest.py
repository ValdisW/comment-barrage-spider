#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import requests

headers = {
    'Host': 'www.bilibili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'fts=1508229812; pgv_pvi=7374468096; rpdid=oqqwsmxwqpdoswqiilmqw; LIVE_BUVID=2988c862a6b9d72a34c05e964228b6bb; LIVE_BUVID__ckMd5=d11b8d00613fdb72; im_notify_type_13271717=2; sid=7etdt55i; UM_distinctid=1669ae067512bb-028802226e476e-8383268-144000-1669ae067524cc; _uuid=9797E404-709C-2013-055F-4E300C6854A405039infoc; CURRENT_QUALITY=80; CURRENT_FNVAL=16; stardustvideo=-1; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1546704889,1546777512,1549280995; arrange=matrix; DedeUserID=13271717; DedeUserID__ckMd5=1f5367f5a29d5cb4; SESSDATA=d2d20cb4%2C1553782962%2Cabc9c221; bili_jct=c10b992cadf74d778ed51d07e36c99ca; buvid3=71B33620-4962-4564-AD05-F8CED0AFA73447161infoc; _dfcaptcha=fa5b271726a7f59603b02bdfb18ef722; bp_t_offset_13271717=228899710812017602'
}
res = requests.get('https://www.bilibili.com/video/av31435619?from=search&seid=14520835153932196247', headers=headers)
print(res.content)