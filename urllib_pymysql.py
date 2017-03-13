# !/usr/bin/env/Python3
# - * - coding: utf-8 - * -


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, random, pymysql


def store(title, content):
    if '\"' in content:
        print('\" BUG!')
        content = content.replace('\"', '\\\"')  # 有bug，如果content中含有'"', 会报错!!!因为没加'\'

    cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")" % (title, content))
    # 提交数据，不然无法保存修改的数据
    cur.connection.commit()
    print('Done!')


def getlinks(articleURL):
    f = urlopen('http://en.wikipedia.org'+articleURL)
    soup = BeautifulSoup(f.read(), 'lxml')
    title = soup.find('h1', {'id': 'firstHeading', 'class': 'firstHeading', 'lang': 'en'}).get_text()
    content = soup.find('div', {'id': 'mw-content-text', 'class': 'mw-content-ltr'}).p.get_text()
    # 先把当前article的 title和content(首段) 存入scraping.pages
    store(title, content)
    # 再findAll(new_articleURL)
    linklist = soup.findAll('a', {'href': re.compile(r'^\/wiki\/((?!(\:|Main_page)).)*$')})
    return linklist


if __name__ == '__main__':
    # 创建连接对象conn和光标对象cur
    conn = pymysql.connect(host='127.0.0.1', user='root', password='LA168167Nc@mysql', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute('USE scraping;')
    #
    random.seed(random.random())
    links = getlinks('/wiki/Kevin_Bacon')

    try:
        for i in range(10):
            new_articleURL = links[random.randint(0, len(links)-1)].attrs['href']
            print(new_articleURL)
            links = getlinks(new_articleURL)
    finally:  # 无论是否出现异常，后面都会执行
        conn.close()  # 用完conn和cur后一定要close(),
        cur.close()  # 否则会造成连接泄露，数据库无法关闭，耗费数据库资源
        print('close done!')
