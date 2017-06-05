# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import json
import os
import sys
# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup

# 定义储存文件类型
file_type = {
    u"金融": "finance",
    u"理财": "financing",
    u"基金": "fund",
    u"私募": "private",
    u"股票": "shares",
    u"保险": "insurance",
    u"今日投资": "investment",
}

def get_article_data(html_data):
    # Beautiful Soup处理
    soup = BeautifulSoup(html_data, 'html.parser')

    # 获取类型数据
    type_datas = soup.find_all("div", class_="main-mate")
    if len(type_datas) > 0:
        type_data = type_datas[0]
        try:
            type = type_data.span.get_text()
        except:
            return ''
    else:
        return ''

    # 直接进行数据筛选
    # if file_type.get(type):
    #     pass
    # else:
    #     return ''

    # 获取标题、副标题数据
    title_datas = soup.find_all("div", class_="article-header")
    if len(title_datas) > 0:
        title_data = title_datas[0]
        title = title_data.h1.get_text()
        try:
            sub_title = title_data.p.get_text()
        except:
            sub_title = ''
    else:
        title = ''
        sub_title = ''

    # 获取文章日期数据
    date_datas = soup.find("p", class_="info-s")
    if len(date_datas) > 0:
        for child in date_datas:
            try:
                if child['class'][0] == "date":
                    date = child.get_text()
                    break
                else:
                    date = ''
            except:
                date = ''

    # 获取标签数据
    tag_datas = soup.find_all("a", class_="tags")
    tag_data = []
    for child in tag_datas:
        tag_data.append(child.get_text())
    tags = ','.join(tag_data)

    # 获取正文数据
    content_datas = soup.find_all("div", class_="article-content")
    content_data = []
    for child in content_datas:
        content_data.append(child.get_text())
    # 去除原文链接相关(后续)
    # print content_data
    # try:
    #     content_data.pop()
    # except:
    #     pass
    content = ' '.join(content_data)

    return type, title, sub_title, date, tags, content