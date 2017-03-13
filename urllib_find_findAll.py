#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import request, error
from bs4 import BeautifulSoup


def get_namelist(url):
    try:
        f = request.urlopen(url)
    except (error.HTTPError, error.URLError) as e:
        print(e)
        return None
    try:
        bsobj = BeautifulSoup(f.read(), 'lxml')
        namelist = bsobj.findAll(name='span', attrs={'class': 'green'})
        # findAll <==> find_all        # {'class':('red', 'green')}
    except AttributeError as e:
        print(e)
        return None
    return namelist


if __name__ == '__main__':
    url = 'http://www.pythonscraping.com/pages/warandpeace.html'
    namelist = get_namelist(url)
    if namelist is None:
        print('Name could not be found!')
    else:
        for name in namelist:
            print(name.get_text())

    '''f = request.urlopen(url)
    bsobj = BeautifulSoup(f.read(), 'lxml')
    name = bsobj.find('span', {'class': 'green'})
    # find <==> findAll(find_all)中limit=1的情况
    print(name.get_text())
    '''