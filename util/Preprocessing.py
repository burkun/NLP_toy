'''
@author: Administrator
'''
import Config, os, File
# read data from weibo
fileIO = File.FileIO()
def removeRepeat(files):
    names = {}
    for fileName in files:
        index = fileName.rfind("-")
        right = fileName[fileName.rfind("-")+1:-8]
        newNameLeft = fileName[:index]
        if not names.has_key(right):
            names[right]=fileName
        else:
            oldName = names[right]
            oldNameLeft = oldName[:oldName.rfind("-")]
            if newNameLeft > oldNameLeft:
                names[right] = fileName
    return names
def writeWeiboData():
    outDir = Config.OUTPUTDIR_WEIBO
    inDir = Config.WEIBOPATH
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    dataNameCount = 0
    maxCount = 800000
    curFileName = "data_"+str(dataNameCount)+".txt"
    filesPath = File.FileIO.getDirFiles(inDir)
    filesPath = removeRepeat(filesPath).values()
    c = []
    numFile = len(filesPath)
    curFileNum = 0
    for fp in filesPath:
        contents = fileIO.readFileByPath(fp,"utf-8",File.FileIO.CSVTYPE,(6,))
        c.extend(contents)
        if len(c)>maxCount:
            fileIO.writeData(outDir, curFileName, c)
            dataNameCount += 1
            curFileName = "data_"+str(dataNameCount)+".txt"
            c= [] 
        curFileNum +=1
        print "file:",fp,"remain",numFile-curFileNum
def writeGIGAData():
    inDir = Config.CHINAGIGAWORD
    outDir = Config.OUTPUTDIR_CHINAGIGA
    allGz = File.FileIO.getGzFiles(inDir)
    con = []
    dataNameCount = 0
    curFileNum = 0
    curFileName = "data_"+str(dataNameCount)+".txt"
    numFile = len(allGz)
    maxCount = 100000
    for gz in allGz:
        res = File.FileIO.zipFile(gz)
        entitys = File.StrHelper.getEntity(res)
        con.extend([en.getText() for en in entitys])
        if len(con)>maxCount:
            fileIO.writeData(outDir, curFileName, con)
            dataNameCount += 1
            curFileName = "data_"+str(dataNameCount)+".txt"
            con= []
        curFileNum +=1
        print "file:",gz,"remain",numFile-curFileNum
