#encoding:utf-8
"""
test
test module
"""

#预处理
#import util.Preprocessing as pre
#pre.writeWeiboData()
#pre.writeGIGAData()
# import util.GenUserDic as gen,util.Config as conf
# dataPath = conf.OUTPUTDIR_CHINAGIGA
# dic = gen.UserDic()
# dic.genDic(dataPath)

#减少词典中无关词的个数，没用过
# import util.reduceDic as reduc
# reduc.reduceDic()

#生成新词
# import util.genNewWord as newWord 
# import pickle
# newWord.gen()

import pickle
data = pickle.load(open("newWordDic.pickle"))
for key in data:
    print key, data[key][0]
