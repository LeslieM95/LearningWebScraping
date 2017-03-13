# !/usr/bin/env/Python3
# - * - coding: utf-8 - * -


import requests
import time

# 模拟登陆豆瓣
session = requests.Session()
params = {'form_email': '15614631682', 'form_password': 'LA168170Nc', 'source': 'index_nav', 'redir': 'https://www.douban.com/'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


s1 = session.post('https://accounts.douban.com/login', data=params, headers=headers)
time.sleep(5)
print(s1.text)

# FUCK!第二次运行就不行了，貌似触发了防爬装置，需要输入captcha
# 第二天又成功了三次，之后又要输入captcha
