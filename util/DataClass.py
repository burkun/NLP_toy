#encoding:utf-8
'''
Created on 2013年11月29日

@author: Administrator

'''
class Entity:
    def __init__(self,idStr,typeStr):
        self.idStr = idStr
        self.typeStr = typeStr
        self.headLine = ""
        self.dateLine = ""
        self.text = ""
    def setHeadLine(self,headStr):
        self.headLine = headStr
    def getHeadLine(self):
        return self.headLine
    def setDateLine(self,dateLine):
        self.dateLine = dateLine
    def getDateLine(self):
        return self.dataLine
    def setText(self,text):
        self.text = text
    def getText(self):
        return self.text
    def __str__(self):
        return str(self.idStr+"\n"+self.typeStr+"\n"+self.headLine+"\n"+self.dateLine+"\n"+self.text)