# -*- coding: utf8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xlrd
import xlwt
from datetime import datetime
import xlutils
from xlutils.copy import copy

# excel数据写入
# 输入数据默认为二维数组
def excel_write(fileName, data, path = "./file"):

    # 定义单元格格式
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    # 创建工作表
    wb = xlwt.Workbook()
    # sheetObj = wb.add_sheet('Sheet1')
    sheetObj = wb.sheet_by_name('Sheet1')

    # 获取写入数据的行数
    rowNum = len(data)

    # 写入数据
    # 插入超链接
    # link = 'HYPERLINK("#%s";"%s")' % (str(i), str(i))
    # sheet_index.write(line, 0, xlwt.Formula(link))
    for row in range(rowNum):
        values = []
        colNum = len(data[row])
        for col in range(colNum):
            if col == 1:
                # 对文章标题插入超链接
                # link = 'HYPERLINK("#%s";"%s")' % (data[row][col], data[row][col + 1])
                link = 'HYPERLINK("%s";"%s")' % (data[row][col + 1], data[row][col])
                sheetObj.write(row, col, xlwt.Formula(link))
            elif col == 2:
                pass
            else:
                sheetObj.write(row, col, data[row][col])

    # 文件存储
    filePath = os.path.join(path, fileName)
    wb.save(filePath)

# excel数据读取
def excel_read(fileName, path = "./file"):
    filePath = os.path.join(path, fileName)
    wb = xlrd.open_workbook(filePath)
    # 获取工作簿的个数
    sheetNum = wb.nsheets
    # 获取所有工作薄的名称
    sheetName = wb.sheet_names()
    # 获取指定工作薄(索引)
    sheetObj = wb.sheet_by_index(0)
    # 获取指定工作薄(按名称)
    #sheetObj = wb.sheet_by_name('Sheet1')
    # 获取指定工作薄的行数
    rowNum = sheetObj.nrows
    # 获取指定工作薄的列数
    colNum = sheetObj.ncols

    # 指定数据输出
    # data = []
    # for row in range(rowNum):
    #     values = []
    #     for col in range(colNum):
    #         values.append(str(sheetObj.cell(row, col).value))
    #     print ','.join(values)
    #     data.append(values)
    # return data

    # 仅返回指定行数,对象
    w_xls = copy(wb)
    return rowNum, colNum, w_xls


# excel数据追加
# 输入数据默认为二维数组
def excel_add(fileName, data, path = "./file"):

    # 获取当前文件已有的行数,对象
    curRowNum, curColNum, w_xls = excel_read(fileName, path)
    print curRowNum
    sheet_write = w_xls.get_sheet(0)
    sheet_write.write(curRowNum, curColNum, 'class')

    # 定义单元格格式
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    # 创建工作表
    wb = xlwt.Workbook()
    sheetObj = wb.add_sheet('Sheet1')

    # 获取写入数据的行数
    rowNum = len(data)


    # 写入数据
    # 插入超链接
    # link = 'HYPERLINK("#%s";"%s")' % (str(i), str(i))
    # sheet_index.write(line, 0, xlwt.Formula(link))
    for row in range(rowNum):
        values = []
        colNum = len(data[row])
        for col in range(colNum):
            if col == 1:
                # 对文章标题插入超链接
                # link = 'HYPERLINK("#%s";"%s")' % (data[row][col], data[row][col + 1])
                try:
                    link = 'HYPERLINK("%s";"%s")' % (data[row][col + 1], data[row][col])
                    sheetObj.add(curRowNum + row, col, xlwt.Formula(link))
                except:
                    sheetObj.write(curRowNum + row, col, data[row][col])
                    sheetObj.write(curRowNum + row, col + 1, data[row][col + 1])
            elif col == 2:
                pass
            else:
                sheetObj.write(curRowNum + row, col, data[row][col])

    # 文件存储
    filePath = os.path.join(path, fileName)
    wb.save(filePath)



def add_class():
    wbk = xlwt.Workbook()
    workbook = xlrd.open_workbook('tag_record.xls') #r_xls
    sheet1 = workbook.sheet_by_index(0) #r_sheet
    rows = sheet1.row_values(0)
    cols = sheet1.col_values(20)
    #print len(cols)
    print cols[1]
    print type(cols[1])
    print type('聚类-1')
    #rows_num = sheet1.nrows #50054
    w_xls = copy(workbook)
    sheet_write = w_xls.get_sheet(0)
    sheet_write.write(0,21,'class')
    for i in range(1, len(cols)):
        if cols[i] == u'聚类-1':
            sheet_write.write(i,21,1)
        if cols[i] == u'聚类-2' or cols[i] == u'聚类-4' or cols[i] == u'聚类-6' or cols[i] == u'聚类-11':
            sheet_write.write(i,21,2)
        if cols[i] == u'聚类-3' or cols[i] == u'聚类-5':
            sheet_write.write(i,21,3)
        if cols[i] == u'聚类-8':
            sheet_write.write(i,21,4)
        if cols[i] == u'聚类-9' or cols[i] == u'聚类-10':
            sheet_write.write(i,21,5)
    w_xls.save('tag_record.xls')


def write_append(fileName, data, path):

    filePath = os.path.join(path, fileName)
    r_xls = xlrd.open_workbook(filePath)
    r_sheet = r_xls.sheet_by_index(0)
    rows = r_sheet.nrows
    w_xls = copy(r_xls)
    sheet_write = w_xls.get_sheet(0)

    for col in range(0, len(data)):
        # if col == 1:
        #     # 对文章标题插入超链接
        #     # link = 'HYPERLINK("#%s";"%s")' % (data[row][col], data[row][col + 1])
        #     try:
        #         link = 'HYPERLINK("%s";"%s")' % (data[col + 1], data[col])
        #         sheet_write.write(rows, col, xlwt.Formula(link))
        #     except:
        #         sheet_write.write(rows, col, data[col])
        #         sheet_write.write(rows, col + 1, data[col + 1])
        # elif col == 2:
        #     pass
        # else:
        sheet_write.write(rows, col, data[col])
        # sheet_write.write(rows, i, data[i])

    w_xls.save(filePath)


if __name__ == "__main__":
    # excel_write('example.xls', '')
    # excel_read("example.xls")
    add_class()