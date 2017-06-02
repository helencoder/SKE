#encoding=utf-8

# 解决cmd命令行下输出中文字符乱码问题(必须放置在文本最前面)
from __future__ import unicode_literals
import sys
import json
import os

# 操作中文必须语句，解决字符问题
reload(sys)
sys.setdefaultencoding('utf8')

# 数据清洗(读取用户自定义标签字典，去重)
import codecs
import fileHandle

# 字典文件读取
def dict_read(fileName, path):
    filePath = os.path.join(path, fileName)
    dictFileObject = open(filePath, 'r')  # 进行分词文件的读取
    dictDatas = []
    for line in dictFileObject:
        word = line.strip('\n')  # 去除换行符
        dictDatas.append(word)
    return dictDatas

# jieba字典文件读取
def jieba_dict_read():
    path = 'dict_file/'
    fileName = 'dict.txt.big'
    filePath = os.path.join(path, fileName)
    dictFileObject = open(filePath, 'r')  # 进行分词文件的读取
    dictDatas = []
    for line in dictFileObject:
        wordStr = line.strip('\n')  # 去除换行符
        wordData = wordStr.split(' ')
        word = wordData[0]
        dictDatas.append(word)
    return dictDatas

# 字典文件写入
# 默认方式：追加
def dict_write(data, fileName, path, mode = 'a+'):
    filePath = os.path.join(path, fileName)
    fileObject = codecs.open(filePath, mode, 'utf-8')
    for word in data:
        fileObject.write(word)
        fileObject.write(' ')
        # 字典中词频越高,成词概率越大
        fileObject.write('4')
        fileObject.write(' ')
        fileObject.write('n')
        fileObject.write('\n')
    fileObject.close()

if __name__ == "__main__":
    pass
    # 进行进一步处理（对于其中已经存在于jieba字典中的进行剔除）
    fileName = 'user_dict_back.txt'
    path = 'dict_file/'
    wordDatas = dict_read(fileName, path)
    print len(wordDatas)
    processedWordDatas = list(set(wordDatas))
    jiebaDictWordDatas = jieba_dict_read()
    writeData= []
    for word in processedWordDatas:
        if word in jiebaDictWordDatas:
            print word
            pass
            #processedWordDatas.remove(word)
        else:
            writeData.append(word)

    fileName = 'user_dict.txt'
    dict_write(writeData, fileName, path, mode='r+')
    # print fileData