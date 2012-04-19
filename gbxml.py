from xml.etree.ElementTree import ElementTree, parse, TreeBuilder, SubElement, dump
import os

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

def saveXML(data):
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
    ElementTree(studyguide).write("new.xml")

def listXMLFiles():
    xmlFiles = []
    path = "./xml"
    dirList = os.listdir(path)
    i = 0
    for fname in dirList:
        if fname.endswith(".xml"):
            #print fname
            xmlFiles.append(path + "/" + fname)
            ++i
    return xmlFiles
    
#data = [("Question 1?", ["bla1", "lah1", "lol1"]), ("Question 2?", ["bla2", "lah2", "lol2"])]
#saveXML(data)

#data = loadXML("example.xml")
#for q in data:
#    print q[0]+'\n'
#    for a in q[1]:
#        print '\t' + a + '\n'