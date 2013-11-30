#encode="utf-8"
"""
test
"""
import  os
import codecs
import re
import DataClass
            
class StrHelper:

    """
    helper to find @names
    """
    _RemoveLinkesPattern = re.compile(r"((//<a|<a).*</a>|</a>\r\n|</a>|\r\n)", re.I)
    _RemoveFaceImage = re.compile(r"\[.*\]",re.I)
    _DocFinder = re.compile(r"<DOC.*?>.*?</DOC>",re.I|re.M|re.U|re.DOTALL)
    _DocHeader = re.compile(r'.*<DOC id="(.*)" type="(.*)"',re.I|re.M|re.U|re.DOTALL)
    _DocHeadLine = re.compile(r'.*<HEADLINE>(.*?)</HEADLINE>.*',re.I|re.M|re.U|re.DOTALL)
    _DocDateLine = re.compile(r'.*<DATELINE>(.*)</DATELINE>.*',re.I|re.M|re.U|re.DOTALL)
    _DocText = re.compile(r'.*<TEXT>(.*)</TEXT>.*',re.I|re.M|re.U|re.DOTALL)
    _DocSpace = re.compile(r"\s*",re.I|re.M)
    @staticmethod
    def findAtsNames(rawStr):
        pass
    #StrHelper.removeLinks(lines[index])
    @staticmethod
    def removeLinks(rawStr):
        return StrHelper._RemoveLinkesPattern.sub("",rawStr)
    @staticmethod
    def removeFaceImage(rawStr):
        return StrHelper._RemoveFaceImage.sub("",rawStr)
    @staticmethod
    def getEntity(dataSet):
        docs = StrHelper._DocFinder.findall(dataSet)
        entitys = []
        for doc in docs:
            idStr,typeStr = StrHelper._DocHeader.match(doc).groups()
            headLine = StrHelper._DocHeadLine.match(doc).groups()[0]
            dateLine = StrHelper._DocDateLine.match(doc).groups()[0]
            text = StrHelper._DocText.match(doc).groups()[0].replace("<P>","").replace("</P>","")
            text = StrHelper._DocSpace.sub("",text)
            headLine = StrHelper._DocSpace.sub("",headLine)
            tentity = DataClass.Entity(idStr,typeStr)
            tentity.setHeadLine(headLine)
            tentity.setDateLine(dateLine)
            tentity.setText(text)
            entitys.append(tentity)
        return entitys
class FileIO(object):
    '''
    Helper class for deal with weibo data
    '''
    CSVTYPE = "csv"
    OTHERTYPE = "otherType"
    
    def readFileByPath(self,path,encodeType="utf-8",fileType=CSVTYPE,consern=(2,6,15)):
        fileObj = codecs.open(path,'r', encodeType)
        if fileType == self.CSVTYPE:
            content = []
            for line in fileObj:
                lineArr = []
                lines = line.split(",")
                for index in consern:
                    lineArr.append(StrHelper.removeFaceImage(StrHelper.removeLinks(lines[index])).encode(encodeType))
                content.append(lineArr)
            return content
        else:
            res = fileObj.readlines()
            return "".join(res).replace("\n", "").encode(encodeType)
    
    """
    content is a list or a tuple
    """
    def writeData(self,path,fileName,content):
        fileObj = open(path+fileName, "w")
        for line in content:
            fileObj.write(str(line)+"\n")
        print("Write file"+fileName+"done!")
    
    """
    include dir and files
    """
    @staticmethod
    def getDirFiles(path):
        rawfiles = os.listdir(path)
        files = []
        for fileName in rawfiles: 
            files.append(fileName)
        return files