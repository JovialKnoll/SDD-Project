from xml.etree.ElementTree import ElementTree, parse, TreeBuilder, SubElement, dump
from ftplib import FTP
import os

#Loads a studyguide XML file into a tree structure. 
def loadXML(filename):
    data = []
    success = True
    try:
        studyguide = parse(filename)
    except:
        success = False
    if success:
        questions = studyguide.iter("question")
        i = 0
        for q in questions:
            qAndAPair = [q.text, []]
            data.append(qAndAPair)
            answers = q.iter("answer")
            j = 1
            for a in answers:
                if a.attrib["correct"] == "true":
                    data[i][1].insert(0, a.text)
                else:
                    data[i][1].insert(j, a.text)
                    j += 1
            i += 1
    return data

#Save a studyguide in the format of a tree structure as an XML file. 
def saveXML(data, filename):
    tb = TreeBuilder()
    studyguide = tb.start("studyguide", {})
    
    for dataQuestion in data:
        xmlQuestion = SubElement(studyguide, "question", {})
        xmlQuestion.text = dataQuestion[0]
        for dataAnswer in dataQuestion[1]:
            if dataAnswer == dataQuestion[1][0]:
                xmlAnswer = SubElement(xmlQuestion, "answer", {'correct': "true"})
            else :
                xmlAnswer = SubElement(xmlQuestion, "answer", {'correct':"false"})
            xmlAnswer.text = dataAnswer
            
    #dump(studyguide)
    ElementTree(studyguide).write("xml/" + filename)

#Returns a list of studyguide available locally.
def listLocalXMLFiles():
    path = "xml/"
    return filterFiles(os.listdir(path), path)
	

#Returns a list of studyguide available remotely. 
def listRemoteXMLFiles():
    ftp = FTP("tothemathmos.com")
    ftp.login("gigabright", "learningisfun")
    list = filterFiles(ftp.nlst())
    ftp.quit()
    return list

#Downloads a remote studyguide file by name. 
def download(file):
    success = True
    try:
        ftp = FTP("tothemathmos.com")
        ftp.login("gigabright", "learningisfun")
        ftp.retrbinary("RETR " + file, open("xml/" + file, 'wb').write)
    except:
        success = False
    ftp.quit()
    return success
	
#Uploads a studyguide file to the remote server. 
def upload(file):
    success = True
    print file
    try:
        ftp = FTP("tothemathmos.com")
        ftp.login("gigabright", "learningisfun")
        ftp.storbinary("STOR " + file, open("xml/" + file, "rb"))
        ftp.quit()
    except:
        success = False
    return success

#Filters away anything that doesn't have the xml extention. 
def filterFiles(files, path = ""):
    xmlList = []
    for fname in files:
        if fname.endswith(".xml"):
            xmlList.append(path + fname)
    return xmlList
	
#download("lol.txt")
#upload("example.xml")

#list = listRemoteXMLFiles()
#print list
#list = listLocalXMLFiles()
#print list

#data = [("Question 1?", ["bla1", "lah1", "lol1"]), ("Question 2?", ["bla2", "lah2", "lol2"])]
#saveXML(data)

#data = loadXML("example.xml")
#for q in data:
#    print q[0]+'\n'
#    for a in q[1]:
#        print '\t' + a + '\n'