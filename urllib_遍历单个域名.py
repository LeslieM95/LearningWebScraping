#!/usr/bin/python
# -*- coding: utf-8 -*-

# 遍历单个article域名

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, random, datetime


def get_links(articleURL):
    f = urlopen('https://en.wikipedia.org'+articleURL)

    soup = BeautifulSoup(f.read(), 'lxml')
    linklist = soup.find('div', {'id': 'bodyContent'}).findAll('a', {'href': re.compile(r'^\/wiki\/((?!\:).)*$')})
    return linklist


if __name__ == '__main__':
    # datetime.datetime.now()作为随机数序列生成的起点(random seed)，每次运行都会产生新的随机路径，更具随机性
    random.seed(1)  # 我用random.random()作为random seed也可以
    linklist = get_links('/wiki/Kevin_Bacon')
    while len(linklist) > 0:  # 无限循环
        new_articleURL = linklist[random.randint(0, len(linklist)-1)].attrs['href']
        # link.attrs['href']每次得到的都是相对路径 (如:'/wiki/Kevin_Bacon')
        print(new_articleURL)  # new_articleURL是random.randint()随机得到的
        linklist = get_links(new_articleURL)
        # 把新的词条中得到的链接列表，赋值于linklist变量
        # "linklist = ..."是关键！！！这不是递归，是无限循环！！！
