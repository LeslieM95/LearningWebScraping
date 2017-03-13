# !/usr/bin/env/Python3
# - * - coding: utf-8 - * -


from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os


def get_absurl(baseurl, srcurl):
    # 格式化为绝对路径'http://www.pythonscraping.com/.../...'
    if srcurl.startswith('http://www.'):
        absurl = srcurl
    elif srcurl.startswith('http://'):
        absurl = srcurl[:7] + 'www.' + srcurl[7:]
        # 注意！'http://'是[:7], 不是[:6]
    elif srcurl.startswith('www.'):
        absurl = 'http://' + srcurl
    elif srcurl.startswith('/'):
        absurl = baseurl + srcurl
    else:
        absurl = baseurl + '/' + srcurl
    # 剔除外链
    if baseurl not in absurl:
        return None
    return absurl


def get_downloadpath(absurl, downloadDir):
    # 拼接成完整路径
    path = downloadDir + absurl.replace('http://www.', '')
    if '?' in path:  # 有些url后面带有'?v1.44', 需要把这些去掉
        n = path.find('?')
        path = path[:n]
    # 获取完整目录名，检查是否存在。若不存在，则os.makedirs()创建
    directory = os.path.dirname(path)  # 返回最后一级(file/dir)之前的dirname
    print(path)
    print(directory)
    if not os.path.exists(directory):  # 判断file/dir是否存在
        os.makedirs(directory)  # os.makedirs()创建多级目录；os.mkdir()只能创建一级
                                # 这两个都只能创建文件夹，不能创建文件
    return path


if __name__ == '__main__':
    my_baseurl = 'http://www.pythonscraping.com'
    f = urlopen(my_baseurl)
    soup = BeautifulSoup(f.read(), 'lxml')

    srclist = soup.findAll(lambda tag: 'src' in tag.attrs)
    for src in srclist:
        file_absurl = get_absurl(my_baseurl, src.attrs['src'])
        if file_absurl is not None:
            print(file_absurl)
            download_path = get_downloadpath(file_absurl, 'C:/users/xyeg/desktop/')
            urlretrieve(file_absurl, download_path)
