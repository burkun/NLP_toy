#encoding:utf-8
"""
test
test module
"""
from util.File import FileIO
from util.File import StrHelper

fileIO = FileIO()
contents = fileIO.readFileByPath("data/afp_cmn_200010","utf-8",FileIO.OTHERTYPE)
entity = StrHelper.getEntity(contents)
for e in entity:
    print e

contents = fileIO.readFileByPath("data/test.csv","utf-8",FileIO.CSVTYPE,(6,))
print contents

