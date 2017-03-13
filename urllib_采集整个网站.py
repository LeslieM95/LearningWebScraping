#!/usr/bin/python
# -*- coding: utf-8 -*-


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_links(articleURL):
    global article_links
    f = urlopen('http://en.wikipedia.org'+articleURL)
    soup = BeautifulSoup(f.read(), 'lxml')

    # 收集当前词条的大标题h1, 正文第一段p, 编辑当前词条的Edit链接href
    if soup.h1.get_text() != 'Main Page':  # Main Page不是article，把它剔除
        print(soup.h1.get_text())
        print(soup.find('div', {'id': 'bodyContent'}).p.get_text())
        # 前面两项每个article都有，但有些article不能被编辑
        try:
            print(soup.find('li', {'id': 'ca-edit'}).span.a.attrs['href'])
        except AttributeError as e:
            print('This article can not be edited!')

    # 从主页开始遍历整个网站的所有article
    linklist = soup.find('div', {'id': 'bodyContent'}).\
        findAll('a', {'href': re.compile(r'^\/wiki\/((?!(\:|Main_Page)).)*$')})
        # Main Page不含':', 但也不是article，把它剔除        # (摩根定律)
    for link in linklist:
        if link.attrs['href'] not in article_links:
            new_articleURL = link.attrs['href']
            print('-'*10, new_articleURL, '-'*10)
            article_links.append(new_articleURL)
            get_links(new_articleURL)  # 这才叫递归！！！

if __name__ == '__main__':
    article_links = []
    linklist = get_links('')
    # ''表示从'http://en.wikipedia.org'开始
