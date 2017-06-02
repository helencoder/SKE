#-*- encoding:utf-8 -*-

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import json
import os
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

def details(fileName, path):
    filePath = os.path.join(path, fileName)
    file = codecs.open(filePath, 'a+', 'utf-8')
    text = file.read()

    # 添加自定义文件
    # 结束词、词性、分词标记均可自己定义

    # 词性过滤文件(保留形容词、副形词、名形词、成语、简称略语、习用语、动词、动语素、副动词、名动词、名词)
    ALLOW_SPEECH_TAGS = ['a', 'ad', 'an', 'i', 'j', 'l', 'v', 'vg', 'vd', 'vn', 'n']

    # 关键词处理
    tr4w = TextRank4Keyword(None, ALLOW_SPEECH_TAGS)
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    keyWords = []
    keywords = ''
    for item in tr4w.get_keywords(10, word_min_len=2):
        keyWords.append(item.word)
    # 对返回的关键词进行处理，便于后续写入
    keywords = ('\\').join(keyWords)

    # 关键短语处理
    keyPhrases = []
    keypharses = ''
    for phrase in tr4w.get_keyphrases(keywords_num=10, min_occur_num=2):
        keyPhrases.append(phrase)
    # 对返回的关键短语进行处理，便于后续写入
    keypharses = ('\\').join(keyPhrases)

    # 文本摘要处理
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')

    # 文本摘要提取
    keySentences = {}
    keysentences = []
    abstract = ''
    for item in tr4s.get_key_sentences(num=3):
        keySentences[item.index] = item.sentence

    # 摘要合成处理(需要引入去重处理)
    # sortedKeySentences = sorted(keySentences.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列
    keySentences = sortedDictValues(keySentences)
    for item in keySentences:
        keysentences.append(item)
    # 去重操作
    duplicated_keysentences = duplication(keysentences)
    # 对返回的关键短语进行处理，便于后续写入
    abstract = (',').join(duplicated_keysentences)

    # 数据返回(元组形式)
    return keywords, keypharses, abstract

# dict数据sort排序（key）
def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

# dict数据去重
def duplication(list):
    length = len(list)
    if length >= 2 :
        pass
    else:
        return list

    # 进行查询标记收集，记录那些重复的字符串index
    index_flag = []
    for i in range(len(list)):
        flag = list[i]
        for j in range(len(list)):
            if (i != j) and (flag.find(list[j]) >= 0):
                index_flag.append(j)

    # 先进行index_flag去重
    if(len(index_flag) > 0):
        duplicated_index_flag = sorted(set(index_flag), key=index_flag.index)
        if (len(duplicated_index_flag) == len(list)):
            return list[0]
        else:
            for x in duplicated_index_flag:
                try:
                    del list[x]
                except:
                    pass
    else:
        pass

    return list

if __name__ == "__main__":
    pass

    path = ''
    fileName = 'article2.txt'
    keywords, keypharses, abstract = details(fileName, path)
    print keywords
    # path = file_handle.get_lib_file('stopwords.txt')
    # print(path)

