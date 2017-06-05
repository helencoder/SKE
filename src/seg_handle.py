# encoding=utf-8

import os
import jieba
jieba.load_userdict("./dict_file/dict.txt.big")
import jieba.posseg as pseg
import sys
import operator
import dir_handle

reload(sys)
sys.setdefaultencoding('utf8')

# 词性过滤文件(保留形容词、副形词、名形词、成语、简称略语、习用语、动词、动语素、副动词、名动词、名词)
ALLOW_SPEECH_TAGS = ['a', 'ad', 'an', 'i', 'j', 'l', 'v', 'vg', 'vd', 'vn', 'n']

# 读入文章，分词，写入文件
# flag：True 表明此文件后续会继续被处理，所以只有分词 False，则可以美一点
# 返回分词的数量
def seg_file(originalFilePath, segFilePath, flag = True):
    try:
        # 进行文章的读取
        fileObject = open(originalFilePath, 'r+')
        fileData = fileObject.read()

        # 进行文章的分词操作
        psegList = pseg.cut(fileData)

        # 进行分词文件的创建
        segFileObject = open(segFilePath, 'w')
        # 进行分词数量的记录
        wordCount = 0

        # 进行分词文件的记录
        for line in psegList:
            if line.flag == 'x':
                pass
            else:
                wordCount += 1
                if flag:
                    segFileObject.write(line.word)
                    segFileObject.write('\n')  # 显式写入换行
                else:
                    segFileObject.write(str(wordCount))
                    segFileObject.write('\t')
                    segFileObject.write(line.word)
                    segFileObject.write('\t')
                    segFileObject.write(line.flag)
                    segFileObject.write('\n')   # 显式写入换行

        return wordCount

    finally:
        fileObject.close()
        segFileObject.close()



# 分词后文件记录
# flag:True 降序输出 False 升序输出
def record_file(segFilePath, recordFilePath, totalCount, flag = True):
    try:
        # 计算词频
        segFileObject = open(segFilePath, 'r')  # 进行分词文件的读取
        wordDatas = {}
        for line in segFileObject:
            word = line.strip('\n')  # 去除换行符
            if wordDatas.has_key(word):
                wordDatas[word] = (wordDatas.get(word) + 1)
            else:
                wordDatas[word] = 1
        if flag:
            sortedWordDatas = sorted(wordDatas.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列
        else:
            sortedWordDatas = sorted(wordDatas.items(), key=operator.itemgetter(1))  # 升序排列

        # 进行记录文件的创建
        recordFileObject = open(recordFilePath, 'w')
        recordFileObject.write("当前文章分词后共有单词数量为： ")
        recordFileObject.write(str(totalCount))
        recordFileObject.write('\n')
        for line in sortedWordDatas:
            recordFileObject.write(line[0])
            recordFileObject.write('\t')
            recordFileObject.write(str(line[1]))
            recordFileObject.write('\n')  # 显示写入换行

    finally:
        segFileObject.close()
        segFileObject.close()


# 文件分词记录集中函数
def seg_handle(originalFileName):
    curDir = dir_handle.cur_file_dir()
    originalFilePath = os.path.join(curDir, originalFileName)
    # 根据原始文章名称自动进行分词文件和记录文件的命名
    segFilePath = originalFilePath.strip('.txt') + '_seg.txt'
    print segFilePath
    recordFilePath = originalFilePath.strip('.txt') + '_record.txt'
    wordCount = seg_file(originalFilePath, segFilePath)
    record_file(segFilePath, recordFilePath, wordCount)


# 直接进行数据的分词记录
def seg_data(contentData):
    # 加载停用词文件
    # jieba.analyse.set_stop_words('dict_file/stop_words.txt')
    stopWords = [line.strip().decode('utf-8') for line in open('dict_file/stop_words.txt').readlines()]
    # 进行文章的分词操作
    psegList = pseg.cut(contentData)
    wordDatas = {}
    for word in psegList:
        # 添加关键词长度限制,大于1
        if word.flag in set(ALLOW_SPEECH_TAGS) and word.word not in stopWords and len(word.word) > 1:
            if wordDatas.has_key(word.word):
                wordDatas[word.word] = (wordDatas.get(word.word) + 1)
            else:
                wordDatas[word.word] = 1

    sortedWordDatas = sorted(wordDatas.iteritems(), key=lambda d: d[1], reverse=True)  # 降序排列
    return sortedWordDatas
        # 进行记录文件的创建


if __name__ == "__main__":

    # 文件测试
    originalFileName = 'index_file/gold.txt'
    # seg_handle(originalFileName)

    contentData = u"2012年冬，北京马可波罗酒店门口，两个年轻人正在等车。一辆出租车停在门口，司机探出头，“哪位约的车？”滴滴出行CEO程维摆摆手，得意的看向身旁的美团CEO王兴。就在刚刚结束的饭局上，程维向王兴展示自己的作品“嘀嘀打车”，不料王兴只看了一眼，一盆冷水浇下来，“这个产品注册流程设计的太垃圾，你看看现在的互联网产品，哪里还有需要注册的。”这件旧事，在四年后的乌镇世界互联网大会期间，被重提。王兴已经记忆模糊，“我不习惯用垃圾两个字，当时说用户体验有很多需要改进的地方。”程维笑笑，“其实我也觉得那个设计挺垃圾的。”中国互联网圈王兴对产品很有洞见，之后的故事也佐证了这一点。事后外界才得知，这款被王兴视为“垃圾”的产品，是外包公司找一位山东的中专老师带着学生鼓捣出来的。也正是这个产品让早期的滴滴一时间陷入僵局，直到原百度技术牛人张博加入，并用了近一年时间重新研发打磨产品。两位看似毫无交集的男主角在之后的4年多时间里，上演了两场颇为相似的商战大戏。地推巷战、融资阻击、资本寒冬……最终以合并的方式扫清战场，堪称中国O2O战场的经典战役。2016年将过，这一年里他们完成了跑马圈地的加速狂奔，O2O战局趋稳，行业巨头的头部效应正在显露。但是，战场没有中场休整，下半场已经如约而至。正如王兴引用钱穆的话，“过去未去，未来已来”。没错，移动互联网和互联网是交织在一起的。2017年，王兴和程维又将重新站上“下半场”起跑线。如果说BAT这些互联网前辈已经完成人和信息、信息和信息的连接，搭建起互联网的“水电煤”生态。王兴等互联网“少壮派”完成人与交通工具、人与吃喝玩乐的物理连接后，他们的眼光已经投向“下半场”——技术创业、产业融合和国际化。一场触达传统产业链的化学反应正在发生。大逃杀 2010年，王兴创立美团，并在三年间从“千团大战”“百团大战”中杀出重围，坐稳团购网站头把交椅，随后成长为一个吃喝玩乐一站式服务平台。2012年，程维告别供职八年的阿里巴巴创立滴滴，并用四年时间打造国内最大的出行平台。战事过半，王兴和程维都刚从一场腥风血雨中险胜。回忆起过去的疯狂扩张，王兴不后悔，“快是必要的，竞争在某些时刻是非常残酷的。一个很受触动的片段是，舒马赫和阿隆索在一次最后对决的时候，双方长期齐驱并驾。经过长时间的僵持后，最后阿隆索胜出了。事后别人问他为什么，他说大家都不松的话，可能车毁人亡，他有小孩，我没小孩，他应该会让我。”程维对此高度认同，“双方轮流竞价到一定阶段后，这是一种必然。如果你并不能够靠一直踩油门把对手踩死，也并非一定要车毁人亡才能结束战争，也许还有第三种解决方式。”"
    # 对文章进行词频统计和记录
    wordFrequency = seg_data(contentData)
    # print wordFrequency
    # 对数据进行组织
    frequencyDatas = ''
    wordCount = 0
    for data in wordFrequency:
        if wordCount > 10:
            break
        tmpData = data[0] + '/' + str(data[1]) + ' '
        frequencyDatas += tmpData
        wordCount += 1

    print frequencyDatas