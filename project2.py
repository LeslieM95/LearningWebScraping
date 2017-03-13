# !/usr/bin/env/Python3
# - * - coding:utf-8 - * -


# 模拟登陆豆瓣，抓取电影院正在上映的电影信息，并存储到MySQL


from bs4 import BeautifulSoup
import requests
import pymysql
import time


# 存储到scraping.screening
def store(title, rate, star, duration, region, director, actors):
    cur.execute('INSERT INTO screening (title, rate, star, duration, region, director, actors) \
    VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")' % (title, rate, star, duration, region, director, actors))
    # 提交数据，不然无法保存修改的数据
    cur.connection.commit()


# 获取正在上映的电影列表
def get_screeninglist(url):
    # GET方法，请求登陆后页面中的"https://movie.douban.com/"
    s = session.get(url)
    try:
        soup = BeautifulSoup(s.text, 'lxml')
        screening_list = soup.find('div', {'id': 'wrapper'}).find('div', {'id': 'screening'}).findAll('li', {
            'class': ('ui-slide-item', 'ui-slide-item s'), 'data-enough': ('True', 'False')})
    except AttributeError as e:
        print(e)
        return None
    return screening_list


if __name__ == '__main__':
    # 创建连接对象conn和光标对象cur
    conn = pymysql.connect(host='127.0.0.1', user='root', password='LA168167Nc@mysql', db='mysql', charset='utf8')
    cur = conn.cursor()
    # 创建数据库scraping
    cur.execute('CREATE DATABASE scraping;')
    cur.execute('USE scraping;')
    # 创建scraping中的表screening
    cur.execute('CREATE TABLE screening \
    (id BIGINT(7) NOT NULL AUTO_INCREMENT PRIMARY KEY, \
    title VARCHAR(100) NOT NULL, \
    rate CHAR(3) NOT NULL, \
    star CHAR(2) NOT NULL, \
    duration VARCHAR(100) NOT NULL, \
    region VARCHAR(100) NOT NULL, \
    director VARCHAR(100) NOT NULL, \
    actors VARCHAR(300) NOT NULL, \
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);')

    # 模拟登陆豆瓣
    # 登录信息
    params = {'form_email': '15614631682', 'form_password': 'LA168170Nc'}
    # 用fiddler抓取的浏览器请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    # 创建session实例
    session = requests.Session()
    # 提交登录信息表单，修改请求头，发起POST请求
    s = session.post('https://accounts.douban.com/login', data=params, headers=headers)
    time.sleep(5)
    # 获取正在上映的电影列表
    screenings = get_screeninglist('https://movie.douban.com/')

    if screenings is not None:
        try:
            for movie in screenings:
                title = movie.attrs['data-title']
                rate = movie.attrs['data-rate']
                star = movie.attrs['data-star']
                duration = movie.attrs['data-duration']
                region = movie.attrs['data-region']
                director = movie.attrs['data-director']
                actors = movie.attrs['data-actors']
                # 存储到scraping.screening
                store(title, rate, star, duration, region, director, actors)
        finally:
            cur.close()  # 用完conn和cur后一定要close(),
            conn.close()  # 否则会造成连接泄露，数据库无法关闭，耗费数据库资源
















