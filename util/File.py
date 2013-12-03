# coding=utf-8
"""
test
"""
import  os
import codecs
import re
import DataClass
import gzip            
class StrHelper:

    """
    helper to find @names
    """
    _RemoveLinkesPattern = re.compile(r"((//<a|<a).*</a>|</a>\r\n|</a>|\r\n)", re.I)
    _RemoveFaceImage = re.compile(r"\[.*\]",re.I)
    _DocFinder = re.compile(r"<DOC.*?>.*?</DOC>",re.I|re.M|re.U|re.DOTALL)
    _DocHiperLink = re.compile("http://[a-zA-Z0-9]+\.[a-zA-Z]+/[a-zA-Z0-9]+")
    
    _DocHeader = re.compile(r'.*<DOC id="(.*)" type="(.*)"',re.I|re.M|re.U|re.DOTALL)
    _DocHeadLine = re.compile(r'.*<HEADLINE>(.*?)</HEADLINE>.*',re.I|re.M|re.U|re.DOTALL)
    _DocDateLine = re.compile(r'.*<DATELINE>(.*)</DATELINE>.*',re.I|re.M|re.U|re.DOTALL)
    _DocText = re.compile(r'.*<TEXT>(.*)</TEXT>.*',re.I|re.M|re.U|re.DOTALL)
    _DocSpace = re.compile(r"\s*",re.I|re.M)
    _WeiboRemovedStr="抱歉，此微博"
    _WeiboJuckStr="转发微博"
    _WeiboHeaderStr ="消息内容"
    _DocHTMLCHAR = re.compile(r"&.+;", re.M)
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
            #headLine = StrHelper._DocHeadLine.match(doc).groups()[0]
            #dateLine = StrHelper._DocDateLine.match(doc).groups()[0]
            text = StrHelper._DocText.match(doc).groups()[0].replace("<P>","").replace("</P>","")
            text = StrHelper._DocSpace.sub("",text)
            text = text.lstrip().rstrip()
            #headLine = StrHelper._DocSpace.sub("",headLine)
            tentity = DataClass.Entity(idStr,typeStr)
            #tentity.setHeadLine(headLine)
            #tentity.setDateLine(dateLine)
            tentity.setText(text)
            entitys.append(tentity)
        return entitys
class FileIO(object):
    '''
    Helper class for deal with weibo data
    '''
    CSVTYPE = "csv"
    OTHERTYPE = "otherType"
    
    def readFileByPath(self,path,encodeType="utf-8",fileType=CSVTYPE,consern=(6,)):
        lastLine = ""
        fileObj = codecs.open(path,'r', encodeType)
        if fileType == self.CSVTYPE:
            content = []
            for line in fileObj:
                lineArr = []
                lines = line.split(",")
                for index in consern:
                    if len(lines)<= index or lines[index].find(StrHelper._WeiboRemovedStr)!=-1 or lines[index].find(StrHelper._WeiboJuckStr)!=-1:
                    #抱歉，此微博已被删除。
                        #print("数组下标越界或有垃圾信息")
                        break
                    tempStr = StrHelper.removeLinks(lines[index])
                    tempStr = StrHelper.removeFaceImage(tempStr)
                    tempStr = tempStr.replace("#","").replace('"',"").replace("//@","").replace("@","").replace("【","").replace("】","")
                    tempStr = tempStr.lstrip().rstrip()
                    tempStr = StrHelper._DocHiperLink.sub("",tempStr)
                    tempStr = StrHelper._DocHTMLCHAR.sub("",tempStr)
                    if len(tempStr)!=0 and tempStr != "" and tempStr !=" " and tempStr.find(StrHelper._WeiboHeaderStr)==-1:
                        if lastLine != tempStr:
                            lineArr.append(tempStr.encode(encodeType))
                            lastLine = tempStr #去重
                if len(lineArr)!=0:
                    content.append(lineArr)
            return content
        else:
            res = fileObj.readlines()
            return "".join(res).replace("\n", "").encode(encodeType)
        fileObj.close()
    """
    content is a list or a tuple
    """
    def writeData(self,path,fileName,content):
        fileObj = open(path+fileName, "a")
        for line in content:
            if isinstance(line, list):
                for l in line:
                    fileObj.write(l.encode("utf-8")+" ")
            else:
                fileObj.write(str(line).encode("utf-8"))
            fileObj.write("\n")
        fileObj.flush()
        fileObj.close()
        print("Write file"+fileName+" done!")
    
    """
    get all the files of the first level 
    """
    @staticmethod
    def getDirFiles(path):
        rawfiles = os.listdir(path)
        files = []
        for fileName in rawfiles: 
            rePath = path+fileName
            if not os.path.isdir(rePath):
                files.append(rePath)
        return files
    @staticmethod
    def getFileList(path,listf,typestr):
        subFiles = os.listdir(path)
        for p in subFiles:
            curP = path+"/"+p
            if os.path.isdir(curP):
                FileIO.getFileList(curP,listf,typestr)
            else:
                if p.endswith(typestr):
                    listf.append(curP)
    @staticmethod
    def getGzFiles(path):
        listf = []
        FileIO.getFileList(path,listf,".gz")
        return listf
    @staticmethod
    def zipFile(path):
        fileHandler = gzip.open(path, "rb", 9)
        contents = fileHandler.readlines()
        fileHandler.flush()
        fileHandler.close()
        return "".join(contents).replace("\n", "").encode("utf-8")