# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os

# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

import textRank
import fileHandle
import excel_handle

def record():
    pass

# 此下面的语句被import引入后不会执行
if __name__ == "__main__":
    print 'hello'
    path = 'corpus/'
    fileName = '1000001.txt'
    keywords, keypharses, abstract = textRank.details(fileName, path)
    # 获取标题
    title = fileHandle.get_file_line_details(fileName, path)
    # 获取文章链接
    tag = fileHandle.get_file_third_line_details(fileName, path)

    # 获取文件列表
    fileList = fileHandle.get_file_list(path);
    for file in fileList:
        # 获取标题
        title = fileHandle.get_file_line_details(file, path)
        # 获取标签
        tag = fileHandle.get_file_third_line_details(file, path)
        # 获取关键词和关键短语
        keywords, keypharses, abstract = textRank.details(file, path)
        # 获取文章链接
        flag = str(file).strip('.txt')
        baseurl = 'http://www.jiemian.com/article/%d.html' % (int(flag))

        fileData = []
        fileData.append(title)
        fileData.append(baseurl)
        fileData.append(tag)
        fileData.append(keypharses)
        fileData.append(keywords)
        # print type(title)
        # print type(baseurl)
        # print type(tag)
        # print type(keypharses)
        # print type(keywords)
        excel_handle.write_append('tag_record.xls', fileData, '.')

        print "当前处理文本为：", file


    # 获取文章链接
    # baseurl = 'http://www.jiemian.com/article/%d.html' % (123124)