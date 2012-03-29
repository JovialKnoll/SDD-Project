from xml.etree.ElementTree import ElementTree, TreeBuilder, SubElement, dump

def saveXML(data):
	data[0][1][0];
	tb = TreeBuilder()
	studyguide = tb.start("studyguide", {})
	len(data)
	
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

data = [("Question 1?", ["bla1", "lah1", "lol1"]), ("Question 2?", ["bla2", "lah2", "lol2"])]
saveXML(data)


