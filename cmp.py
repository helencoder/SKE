# encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import json
import os
import sys
# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')
import src.scrapy_handle as scrapy_handle
import src.html_handle as html_handle
import src.file_handle as file_handle
import src.excel_handle as excel_handle
import src.seg_handle as seg_handle
import textRank
import main

# 《界面》文章标签的抓取
tagDatas = []
recordCount = 0
flag = 1353000
# 统计文章标签来源于词频正确率
fileCount = 0
tagCount = 0
while flag <= 1400000:
    baseurl = 'http://www.jiemian.com/article/%d.html' % (flag)
    # 进行文本抓取
    text = scrapy_handle.get_html_data(baseurl)
    # 进行文本信息获取
    if not text:
        flag += 1
        continue
    else:
        # 进行文本信息获取
        article_data = html_handle.get_article_data(text)
        # print article_data

        # 进行文本信息的记录(便于打印输出)
        # type = json.dumps(article_data[0], ensure_ascii=False)
        # title = json.dumps(article_data[1], ensure_ascii=False)
        # sub_title = json.dumps(article_data[2], ensure_ascii=False)
        # date = json.dumps(article_data[3], ensure_ascii=False)
        # tags = json.dumps(article_data[4], ensure_ascii=False)
        # content = json.dumps(article_data[5], ensure_ascii=False)
        # print type, title, sub_title, date, tags, content
        # print type, title, date, tags

        # 若数据为空，不进行记录操作
        if len(article_data) == 0:
            flag += 1
            continue

        # 文章数据记录，便于后续SKE算法实现
        recordFileName = str(flag) + '.txt'
        recordFilePath = 'files/' + str(flag) + '.txt'
        print recordFilePath
        # 仅存储文章标题和正文
        file_handle.write_file(recordFilePath, article_data[1])  # 类型暂时不写入，直接通过文件名区分
        file_handle.write_file(recordFilePath, article_data[2])
        file_handle.write_file(recordFilePath, article_data[5])

        # 文章数据
        path = 'files'
        fileName = recordFileName

        # 统计数据包括类别、文章标题、文章链接、文章标签、SKE算法标签、TextRank算法标签

        # textRank 算法统计
        keywords, keypharses, abstract = textRank.details(fileName, path)
        print keywords
        # 进行textrank关键词数据处理
        textrankKeywords = keywords

        # SKE算法统计
        ske = main.main(fileName, path)
        print json.dumps(ske, ensure_ascii=False)
        # 进行ske关键词的数据处理
        skeKeywordsData = ske[0:9]  #top10
        skeKeywordsList = []
        for data in skeKeywordsData:
            skeKeywordsList.append(data[0])
        skeKeywords = '\\'.join(skeKeywordsList)
        print skeKeywords

        # 词频算法统计
        wordFrequency = seg_handle.seg_data(article_data[5])
        # 对数据进行组织
        frequencyDatasList = []
        wordCount = 0
        # TOP10
        for data in wordFrequency:
            if wordCount > 10:
                break
            tmpData = data[0] + '/' + str(data[1]) + ' '
            frequencyDatasList.append(data[0])
            wordCount += 1
        # 进行词频关键词的数据处理
        frequencyDatas = '\\'.join(frequencyDatasList)
        print frequencyDatas
        frequencyKeywords = frequencyDatas

        # 文章原始标签
        tagList = article_data[4].split(',')
        # 标签正确率统计
        skeCount = 0
        textrankCount = 0
        frequencyCount = 0
        for tag in tagList:
            if len(tag) == 0:
                continue
            else:
                skeFlag = skeKeywords.find(tag)
                textrankFlag = textrankKeywords.find(tag)
                frequencyFlag = frequencyKeywords.find(tag)
                if skeFlag > 0:
                    skeCount += 1
                if textrankFlag > 0:
                    textrankCount += 1
                if frequencyFlag > 0:
                    frequencyCount += 1

        print skeCount, textrankCount, frequencyCount

        # 计算flag(查找其中正确率最高的)
        maxNum = max(skeCount, textrankCount, frequencyCount)
        flagList = []
        if maxNum == 0:
            flagList.append('null')
        else:
            if maxNum == skeCount:
                flagList.append('ske')
            if maxNum == textrankCount:
                flagList.append('textrank')
            if maxNum == frequencyCount:
                flagList.append('frequency')
        curflag = '\\'.join(flagList)


        # 进行数据记录textrankKeywords
        tagData = [article_data[0], article_data[1], baseurl, article_data[4], skeKeywords, textrankKeywords, frequencyKeywords, str(skeCount), str(textrankCount), str(frequencyCount), curflag]
        tagDatas.append(tagData)
        excel_handle.write_append('results.xls', tagData, '.')


        fileCount += 1
        print "当前已处理文章数为： ", fileCount
        # if fileCount >= 1:
        #     break


    flag += 1

# 进行文件记录
# excel_handle.excel_write('tag_record_back.xls', tagDatas, '.')