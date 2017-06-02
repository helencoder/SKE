# encoding=utf-8

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


# 获取文件列表（该目录下放着100份文档）
def getCorpusFilelist(path = 'corpus'):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if (f[0] == '.'):
            pass
        else:
            # filelist.append(os.path.join(path, f))
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

    # 将分词后的结果用空格隔开，保存至本地。比如"我来到北京清华大学"，分词结果写入为："我 来到 北京 清华大学"
    #f = open(sFilePath + "/" + filename + "-seg.txt", "w+")
    recordFileName = segFileName.strip('.txt') + '_seg.txt'
    recordFilePath = os.path.join(recordPath, recordFileName)
    f = open(recordFilePath, "w+")
    f.write(' '.join(result))
    f.close()


# 读取100份已分词好的文档，进行TF-IDF计算
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
    weight = tfidf.toarray()  # 对应的tfidf矩阵\

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
        # 进行文件存储
        flag = 0
        for line in sortedWordDatas:
            if flag < count:
                keywordData.append(line[0])
            # f.write(line[0])
            # f.write('\t')
            # f.write(str(line[1]))
            # f.write('\n')  # 显示写入换行
            flag += 1
        keywordDatas[segFileNameList[i][:-8]] = keywordData
        # f.close()
    return keywordDatas, segDatas

if __name__ == "__main__":
    # (allfile, path) = getFilelist(sys.argv)
    # for ff in allfile:
    #     print "Using jieba on " + ff
    #     fenci(ff, path)
    # Tfidf(allfile)
    # fileList = getCorpusFilelist()
    # for file in fileList:
    #     print "Using jieba on " + file
    #     segFile(file)
    segFileNameList = getCorpusFilelist('segFile')
    keywordDatas, segDatas = Tfidf(segFileNameList)
    print keywordDatas
    print keywordDatas.get('financing_1224323')