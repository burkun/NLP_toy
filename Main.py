#encoding:utf-8
"""
test
test module
"""

#预处理
#import util.Preprocessing as pre
#pre.writeWeiboData()
#pre.writeGIGAData()
pp = "E:\ChinaGIGA\data_0.txt"
def cuttest(test_sent):
    result = jieba.cut(test_sent)
    print " / ".join(result)
import jieba
from util.File import FileIO

res = FileIO.readProFile(pp)


cuttest(res[0])