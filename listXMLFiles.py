import os

def listXMLFiles():
	xmlFiles = []
	path = "./xml"
	dirList = os.listdir(path)
	i = 0
	for fname in dirList:
		if fname.endswith(".xml"):
			#print fname
			xmlFiles.append(fname)
			++i
	return xmlFiles
		