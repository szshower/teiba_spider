#!/usr/bin/env python
# coding: utf-8

import os
import urllib
import urllib2
import re


def get_page_info(url):
    info = []
    headers = {

        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'tieba.baidu.com',
    }
    try:
        content = urllib2.urlopen(urllib2.Request(url, headers=headers)).read()  # 获取页面内容
        pattern = re.compile('(href="/home/main/\?un=)(.*?)(&ie=utf-8)')  # 正则规则
        items = re.findall(pattern, content)  # 正则匹配
        for i in range(len(items)):
            name = urllib.unquote(items[i][1].encode('utf-8'))  # 编码转换为中文
            info.append((name, items[i][1]))  # 保存在新的列表
        info = list(set(info))  # 列表去重
        print ('一共%s个头像'%len(info))
        return info
    except urllib2.HTTPError as e:
        print e
        exit()
    except urllib2.URLError as e:
        print e
        exit()


def get_page_portrait(info, url):
    for i in range(len(info)):
        print('解析中：'+str((i+1))+'/'+str(len(info)))
        portrait_code_url = 'http://tieba.baidu.com/home/get/panel?ie=utf-8&un=' + info[i][1]#获取动态加载页面内容
        headers = {

            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'tieba.baidu.com',
            'Referer': url
        }
        try:
            content = urllib2.urlopen(urllib2.Request(portrait_code_url, headers=headers)).read()  # 获取页面内容
            pattern = re.compile('(portrait":")(.*?)(",)')  # 正则规则
            items = re.findall(pattern, content)  # 正则匹配
            info[i] = list(info[i])
            info[i].extend([items[0][1], 'https://gss0.bdstatic.com/6LZ1dD3d1sgCo2Kml5_Y_D3/sys/portrait/item/' + items[0][1]])#把真正的头像链接加入列表
        except urllib2.HTTPError as e:
            print e
            exit()
        except urllib2.URLError as e:
            print e
            exit()
    portrait_info = info
    return portrait_info

def download_image(portrait_info):
    print('开始下载')
    if not os.path.exists('portrait_img'):#创建文件目录
        os.makedirs('portrait_img')
    for i in range(len(portrait_info)):
        portrait_url=portrait_info[i][3]
        portrait_name=portrait_info[i][0]

        urllib.urlretrieve(portrait_url,'portrait_img/'+portrait_name.decode('utf-8')+'.jpg')#下载图片并保存
        print ('download  %s  successful!'%portrait_url)
    print ('下载完毕')


if __name__ == "__main__":
    url = 'http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5'
    info = get_page_info(url)
    portrait_info =get_page_portrait(info, url)
    download_image(portrait_info)

