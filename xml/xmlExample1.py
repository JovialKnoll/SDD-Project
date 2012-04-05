#http://docs.python.org/library/xml.etree.elementtree.html

from xml.etree.ElementTree import ElementTree, parse

studyguide = parse("example.xml")
questions = studyguide.iter("question")
for q in questions:
	print q.text
	answers = q.iter("answer")
	for a in answers:
		if a.attrib["correct"] == "true":
			print a.text
	print '\n'
#dump(tree)


