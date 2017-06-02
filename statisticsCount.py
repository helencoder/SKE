#encoding=utf-8

# 词语统计特征值计算

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import os
import json
import jieba
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import textPreprocessing
import fileHandle

# 词语词性值权重分配
pos = {
    'a':  0.5,
    'ad': 0.3,
    'an': 0.6,
    'i':  0.6,
    'j':  0.7,
    'l':  0.6,
    'v':  0.3,
    'vg': 0.2,
    'vd': 0.4,
    'vn': 0.6,
    'n':  0.8
}

# 依据指定词性对于词语进行重新记录
# 返回数据格式:
#   {'word': {loc, pos}, ...}
def wordsStatistics(wordsStatisticsData):
    print '------当前进行词语词性权重统计操作------'
    # 进行单词词性标注统计
    for key in wordsStatisticsData:
        wordsStatisticsData[key][1] = pos.get(wordsStatisticsData[key][1])
    return wordsStatisticsData


# 对语料库所有文章进行tfidf计算
def tfidf():
    print '------当前进行词语TF-IDF统计值计算操作------'
    fileList = getCorpusFilelist()
    for file in fileList:
        print "Using jieba on " + file
        segFile(file)
    segFileNameList = getCorpusFilelist('segFile')
    keywordDatas = Tfidf(segFileNameList)
    return keywordDatas


# 获取指定语料库文件列表
def getCorpusFilelist(path = 'corpus'):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if (f[0] == '.'):
            pass
        else:
            filelist.append(f)
    return filelist


# 对文档进行分词处理
def segFile(segFileName, recordPath = 'segFile', filePath = 'corpus'):
    # 保存分词结果的目录
    if not os.path.exists(recordPath):
        os.mkdir(recordPath)
    # 读取文档
    segFilePath = os.path.join(filePath, segFileName)
    fileObj = open(segFilePath, 'r+')
    fileData = fileObj.read()
    fileObj.close()

    # 对文档进行分词处理，采用默认模式
    segFileData = jieba.cut(fileData, cut_all=True)

    # 对空格，换行符进行处理
    result = []
    for data in segFileData:
        data = ''.join(data.split())
        if (data != '' and data != "\n" and data != "\n\n"):
            result.append(data)

    # 将分词后的结果用空格隔开，保存至本地。
    recordFileName = segFileName.strip('.txt') + '_seg.txt'
    recordFilePath = os.path.join(recordPath, recordFileName)
    f = open(recordFilePath, "w+")
    f.write(' '.join(result))
    f.close()


# 读取已分词好的文档，进行TF-IDF计算
def Tfidf(segFileNameList, count = 10, segFilePath = 'segFile'):
    # 保留分词结果
    segDatas = {}
    keywordDatas = {}
    # 存取100份文档的分词结果
    corpus = []
    for fileName in segFileNameList:
        filePath = os.path.join(segFilePath, fileName)
        fileObj = open(filePath, 'r+')
        content = fileObj.read()
        fileObj.close()
        corpus.append(content)
        segDatas[fileName] = content

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()  # 对应的tfidf矩阵

    tfidfPath = 'tfidfFile'
    if not os.path.exists(tfidfPath):
        os.mkdir(tfidfPath)

    # 这里将每份文档词语的TF-IDF写入tfidffile文件夹中保存
    # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for i in range(len(weight)):
        print u"--------Writing all the tf-idf in the", i, u" file into --------"
        tfidfFileName = segFileNameList[i][:-8] + '_tfidf.txt'
        # 暂不进行文件的写入，只进行关键值的记录
        # tfidfFilePath = os.path.join(tfidfPath, tfidfFileName)
        # f = open(tfidfFilePath, 'w+')
        wordDatas = {}
        for j in range(len(word)):
            # 进行排序输出
            wordDatas[word[j]] = weight[i][j]
            # f.write(word[j] + "    " + str(weight[i][j]) + "\n")
        sortedWordDatas = sorted(wordDatas.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列

        # 提取指定个数的关键词
        keywordData = []
        flag = 0
        for line in sortedWordDatas:
            if flag < count:
                keywordData.append(line[0])
            # 文件写入
            # f.write(line[0])
            # f.write('\t')
            # f.write(str(line[1]))
            # f.write('\n')  # 显示写入换行
            flag += 1
        keywordDatas[segFileNameList[i][:-8]] = keywordData
        # f.close()
    return sortedWordDatas


if __name__ == "__main__":
    pass
    keywordDatas = tfidf()
    print keywordDatas
