# encoding=utf-8

from __future__ import unicode_literals
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import codecs

# 定义储存文件类型
type = {
    u"商业": "business",
    u"证券": "securities",
    u"金融": "finance",
    u"投资": "investment",
}

#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

# 检测字符串中是否包含中文字符
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u"\u4e00" <= ch <= u"\u9fff":
            return True
    return False

# 获取指定文件夹下所有文件
# 默认处理当前文件夹相对路径
def get_file_list(path):
    curDir = cur_file_dir()
    filePath = os.path.join(curDir, path)
    print filePath
    fileList = []
    files = os.listdir(filePath)
    for file in files:
        #f = f.decode()
        if (file[0] == '.'):
            pass
        else:
            fileList.append(file)
    return fileList

# 获取指定文件(默认为lib下的文件)

# 获取自定义文件
def get_lib_file(fileName, path = 'lib'):
    dir = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(path, fileName)
    return os.path.join(dir, filePath)


# 获取文件指定行(第一行)
def get_file_line_details(filename):
    curDir = cur_file_dir()
    filePath = os.path.join(curDir, filename)
    file = codecs.open(filePath, 'r', 'utf-8')
    text = file.readline()
    return str(text).strip()

# 写文件操作(默认为追加)
def write_file(filename, data, mode = 'a+'):
    curDir = cur_file_dir()
    filePath = os.path.join(curDir, filename)
    fileObject = codecs.open(filePath, mode, 'utf-8')
    fileObject.write(str(data))
    fileObject.write('\n\n')
    fileObject.close()

# 写入excel文件操作
def write_excel_file():
    pass


if __name__ == "__main__":
    # 文件测试
    path = 'index_file/article.txt'
    #path = './corpus'
    details = get_file_line_details(path)
    details = '《' + details + '》'
    print details

    recordFileName = 'record.txt'
    fileList = get_file_list('corpus')
    for file in fileList:
        filePath = 'corpus/' + file
        details = get_file_line_details(filePath)
        details = '《' + details + '》'
        write_file(recordFileName, details)
        print filePath

    # recordFileName = 'record.txt'
    # write_file(recordFileName, details)
