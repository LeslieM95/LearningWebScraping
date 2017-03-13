# !/usr/bin/env/Python3
# - * - coding:utf-8 - * -


# 抓取图灵社区所有图书中，推荐数排名前100的图书信息，并保存为CSV文件


from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv


# 获得每一页的rowslist
def get_rows(baseurl, page):

    try:
        if page == 0:
            html = urlopen(baseurl)
        else:
            html = urlopen(baseurl+'&page=%s' % page)  # 注意！要把实体引用"&amp;"改为字符"&"
    except (HTTPError, URLError) as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html.read(), 'lxml')
        rowslist = soup.findAll('div', {'class': 'row book-item'})
    except AttributeError as e:
        print(e)
        return None
    return rowslist


# 获得每一行的cellslist
def get_cells(row):
    try:
        cellslist = row.findAll('div', {'class': ('votes', 'answered', 'views-orange')})
        cellslist.append(row.find('div', {'class': 'span6'}).h3)
        cellslist.append(row.find('div', {'class': 'status-date'}))
        cellslist.append(row.findAll('p')[0])
        cellslist.append(row.findAll('p')[1])
    except AttributeError as e:
        print(e)
        return None
    return cellslist


if __name__ == '__main__':
    baseurl = 'http://www.ituring.com.cn/book?sort=vote'
    count = 0
    # 创建csv文件，并写入
    with open('c:/users/xyeg/desktop/booklist.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(('序号', '书名', '是否有电子书', '推荐数', '评论数', '阅读数', '著/译者', '出版日期', '标签'))
        # 对每一页迭代, 获得每一页的rowslist
        for i in range(154):
            # 当count>=100时，跳出"for i in range(154):"循环
            if count >= 100:
                break
            rows = get_rows(baseurl, i)
            # 对每一行迭代, 获得每一行的cellslist
            if rows is not None:
                for row in rows:
                    per_row = []  # 对每一行中每一元素(即cell)处理之后，重新组成一个新的
                    cells = get_cells(row)
                    # 对每一单元格迭代
                    if cells is not None:
                        # append序号
                        count += 1
                        per_row.append(count)
                        # append书名
                        per_row.append(cells[3].a.get_text())
                        # append是否有电子书
                        if cells[3].span is None:
                            per_row.append('否')
                        else:
                            per_row.append('是')
                        # append推荐数
                        per_row.append(cells[0].strong.get_text())
                        # append评论数
                        per_row.append(cells[1].strong.get_text())
                        # append阅读数
                        per_row.append(cells[2].get_text()[:-2])
                        # append著译者
                        authorName = cells[4].get_text()[:-19]
                        per_row.append(authorName.replace(' ', ''))
                        # append出版日期
                        per_row.append(cells[4].get_text()[-19:])  # '2012-08-27'后面有9个空格，如:'2012-08-27         '
                        # append标签
                        tagslist = cells[6].findAll('a')
                        tagstr = ''
                        for tag in tagslist:
                            tagstr = tagstr + tag.get_text() + '/'
                        per_row.append(tagstr.strip('/'))
                        # append摘要
                        # per_row.append(cells[5].get_text())
                    # 把书的信息按航写入csvFile
                    writer.writerow(per_row)
                    # 当count>=100时，跳出"for row in rows:"循环
                    if count >= 100:
                        break







