#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import re
import urllib.request
import time
import urllib.error

#模拟成浏览器
headers = {
    'Host': 'weixin.sogou.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'ABTEST=0|1553662915|v1; IPLOC=CN3202; SUID=7969D63A3E18960A000000005C9B03C3; SUID=7969D63A2D18960A000000005C9B03C3; weixinIndexVisited=1; SUV=007F9A373AD669795C9B03CA3FF86619; JSESSIONID=aaakAFBpcHDRc5EQmBDNw; PHPSESSID=09rtlufll9pdjuqb7qascbcnu7; SUIR=879790FF2224A7F6036BFB2B22733B21; SNUID=388D14A582870455ADD4197D82B0CC89; sct=7'
}


#设置一个列表 listurl 存储文章网址列表
listurl=[]

# 使用代理服务器打开url
def use_proxy(proxy_addr,url):
    print('正在以'+proxy_addr+'打开：'+url)
    #建立异常处理机制
    try:
        import urllib.request
        print('准备代理...')
        proxy= urllib.request.ProxyHandler({'http':proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        opener.addheaders = headers
        urllib.request.install_opener(opener)

        print('尝试打开...')
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        print('打开时URLError:')
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        #若为 URLError 异常，延时10秒执行
        time.sleep(10)
        return ''
    except Exception as e:
        print('打开时Error:')
        print("exception:"+str(e))
        #若为 Exception 异常，延时1秒执行
        time.sleep(1)
        return ''

# 获取所有文章链接
def getlisturl(key,pagestart,pageend,proxy):
    try:
        keycode=urllib.request.quote(key)   # 关键词编码

        #循环爬取各页的文章链接
        for page in range(pagestart,pageend+1):
            url = "http://weixin.sogou.com/weixin?type=2&query="+keycode+"&page="+str(page)

            #用代理服务器爬取，解决 IP 被封杀问题
            data1 = use_proxy(proxy, url)
            print('获得数据:' + data1)

            #获取文章链接的正则表达式
            listurlpat='<div class="txt-box">.*?(http:// .*?)"'

            #获取每页的所有文章链接并添加到列表 listurl 中
            listurl.append(re.compile(listurlpat,re.S).findall(data1))
        print("共获取到"+str(len(listurl))+"页") #便于调试
        return listurl
    except urllib.error.URLError as e:
        print('URLError:')
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        #若为 URLError 异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('Error:')
        print("exception:"+str(e))
        #若为 Exception 异常，延时1秒执行
        time.sleep(1)

# 通过文章链接获取对应内容
def getcontent(listurl,proxy):
    i=0
    #设置本地文件中的开始 html 编码
    html1='''<!DOCTYPE html PUBLIC "-// W3C// DTD XHTML 1.0 Transitional// EN" "http:// 
    www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http:// www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>微信文章页面</title>
</head>
<body>'''
    fh=open("./1.html","wb")
    fh.write(html1.encode("utf-8"))
    fh.close()
    #再次以追加写入的方式打开文件，以写入对应文章内容
    fh=open("./1.html","ab")
    #此时 listurl 为二维列表，形如 listurl[][],第一维存储的信息跟第几页相关，第二维存的跟该页第几个文章链接相关
    for i in range(0,len(listurl)):
        for j in range(0,len(listurl[i])):
            try:
                url=listurl[i][j]
                #处理成真实 url，读者亦可以观察对应网址的关系自行分析，采集网址比真实网址多了一串 amp
                url=url.replace("amp;","")
                #使用代理去爬取对应网址的内容
                data=use_proxy(proxy,url)
                #文章标题正则表达式
                titlepat="<title>(.*?)</title>"
                #文章内容正则表达式
                contentpat='id="js_content">(.*?)id="js_sg_bar"'
                #通过对应正则表达式找到标题并赋给列表 title
                title=re.compile(titlepat).findall(data)
                #通过对应正则表达式找到内容并赋给列表 content
                content=re.compile(contentpat,re.S).findall(data)
                #初始化标题与内容
                thistitle="此次没有获取到"
                thiscontent="此次没有获取到"
                #如果标题列表不为空，说明找到了标题，取列表第零个元素，即此次标题赋给变量 thistitle
                if(title!=[]):
                    thistitle=title[0]
                if(content!=[]):
                    thiscontent=content[0]
                #将标题与内容汇总赋给变量 dataall
                dataall="<p>标题为:"+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>"
                #将该篇文章的标题与内容的总信息写入对应文件
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i)+"个网页第"+str(j)+"次处理") #便于调试
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                #若为 URLError 异常，延时10秒执行
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                #若为 Exception 异常，延时1秒执行
                time.sleep(1)
    fh.close()
    #设置并写入本地文件的 html 后面结束部分代码
    html2='''</body>
</html>
    '''
    fh=open("./1.html","ab")
    fh.write(html2.encode("utf-8"))
    fh.close()

#设置关键词
key="物联网"

#设置代理服务器，该代理服务器有可能失效，读者需要换成新的有效代理服务器
proxy="218.60.8.83:3129"

#可以为 getlisturl()与 getcontent()设置不同的代理服务器，此处没有启用该项设置
proxy2=""

#起始页
pagestart=1

#爬取到哪页
pageend=2

listurl = getlisturl(key,pagestart,pageend,proxy)
getcontent(listurl,proxy)