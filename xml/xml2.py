
from xml.etree.ElementTree import ElementTree, TreeBuilder, SubElement, dump

tb = TreeBuilder()
studyguide = tb.start("studyguide", {})
q1 = SubElement(studyguide, "question", {})
q1.text = "What?!"
a1 = SubElement(q1, "answer", {'correct': "true"})
a1.text = "Right!"
a2 = SubElement(q1, "answer", {'correct': "false"})
a2.text = "Wrong..."
#tb.close("studyguide")
dump(studyguide)
ElementTree(studyguide).write("new.xml")