#!/usr/bin/env python
# -*-coding:utf-8-*-
# zabbix version : 2.4.4
# python version : 2.7.8
import requests
import datetime
import time
from bs4 import BeautifulSoup

# 提交登录信息的url
login_url = 'http://172.16.1.101/index.php'
# 编辑要提交的信息的字典
login_dic = {
                'name': 'admin',
                'password': 'zabbix',
                'autologin': 1,
                'enter': 'Sign in'
            }
# 通过post方式提交登录数据
s = requests.post(url=login_url, data=login_dic)
# 获取服务端分配的cookie字典
user_cookie = s.cookies.get_dict()
# 通过content方法获得登录之后页面的全部html代码
html = s.content
# 通过BeautifulSoup分析获得的页面代码
soup = BeautifulSoup(html, 'html.parser')
# 找出html代码中id为sid标签项目，并通过attrs获取对应的input标签的value值
sid = soup.find(id='sid').attrs['value']
# 获得13位时间戳（很多程序时间戳都是13位的）
curtime = int(time.time()*1000)
# 获取当前的系统时间
now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# 定义获取图形的url
graph_url = 'http://172.16.1.101/chart2.php'
# 通过页面得知要获取流量图需要提供很多参数
graph_dic = {
    'graphid': 994,
    'period': 3600,
    'stime': now_time,
    'height': 200,
    'width': 800,
    'sid': sid,
    'updateProfile': 1,
    'profileIdx': 'web.screens',
    'profileIdx2': 994,
    'screenid': '',
    'curtime': curtime
}
# 提交图形请求时携带的request header内容
graph_header={
    'Host': '172.16.1.101',
    'Referer': 'http://172.16.1.101/charts.php?graphid=994',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}
# 通过get方式访问指定图片的url，带着前面设置的参数
resp = requests.get(url=graph_url, params=graph_dic, headers=graph_header, cookies=user_cookie)
# 将返货的content内容保存为png图片
with open('2.png', 'wb') as f:
    for i in resp.content:
        f.write(i)
