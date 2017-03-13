# !/usr/bin/env/Python3
# - * - coding: utf_8 - * -


from urllib import request, error
from bs4 import BeautifulSoup

# 第一种写法
'''try:
    f = request.urlopen('http://www.pythonscraping.com/pages/page1.html')
except (error.HTTPError, error.URLError) as e:  # 防止网页在服务器上不存在
    print(e, '1')
else:
    if f is None:  # 防止服务器不存在，会返回一个None
        print('URL is not found', '2')
    else:
        try:
            bsobj = BeautifulSoup(f.read(), 'lxml')
            title = bsobj.head.title
        except AttributeError as e:  # bsobj为None，或者bsobj.head为None时，抛出AttributeError
            print(e)
        else:
            print(bsobj.title.get_text())'''


# 第二种写法，没有那么多嵌套，易读性更好！
def title_get(url):
    try:
        f = request.urlopen(url)
    except (error.HTTPError, error.URLError) as e:  # 防止HTTPError:网页在服务器上不存在，或获取页面时出现错误
        print(e)                                    # 和URLError：URL写错了
        return None  #
    try:
        bsobj = BeautifulSoup(f.read(), 'lxml')  # 防止服务器不存在，f为None
        title = bsobj.head.title
        # bsobj.tagname只能所有内容中的第一个符合要求的标签
    except AttributeError as e:  # f为None，bsobj为None，或者bsobj.head为None时，抛出AttributeError
        print(e)
        return None
    return title  # title也可能是None

title = title_get('http://www.pythonscraping.com/pages/page1.html')
if title is None:  # 以上各种错误，最终都会导致title为None
    print('Title is not found!')
else:
    print(title.get_text())