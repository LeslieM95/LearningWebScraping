# !/usr/bin/env/Python3
# - * - coding: utf-8 - * -


from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv


def get_rowslist(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html.read(), 'lxml')
        rowslist = soup.find('table', {'id': 'giftList'}).findAll('tr')
    except AttributeError as e:
        print(e)
        return None
    return rowslist


def get_cellslist(row):
    try:
        cellslist = row.findAll(['td', 'th'])
    except AttributeError as e:
        print(e)
        return None
    return cellslist


if __name__ == '__main__':

    my_url = 'http://www.pythonscraping.com/pages/page3.html'
    rows = get_rowslist(my_url)

    with open('c:/users/xyeg/desktop/gifts.csv', 'w', newline='') as csvFile:
        # 创建writer实例                    # 若没有"newline=''", 每行会多出一行空行
        writer = csv.writer(csvFile)  # 因为单元格中的str前后各有一个'\n'

        if rows is not None:
            for row in rows:
                per_row = []
                cells = get_cellslist(row)
                # 把每个cell中的标签去掉，获得text
                if cells is not None:
                    for cell in cells:
                        if cell.get_text() == '\nImage\n':  # 注意!!!是'\nImage\n', 不是'Image'!!!
                            continue  # 因为这里'\nImage\n'在最后，故continue或break没差别
                        per_row.append(cell.get_text())
                print(per_row)  # ['\nItem Title\n', '\nDescription\n', '\nCost\n']
                writer.writerow(per_row)  # tuple or list



