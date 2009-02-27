import os
from pyPdf import PdfFileReader

'''
If something screws up, we return empty string.
TODO:
# add more doc formats like html, rtf, openoffice etc
# handle all exceptions
# make sure we have doc or pdf headers to prevent storing of malformed input
# warning: all file handlers are django file objects, not python file objects.
badri.dilbert@gmail.com
'''

def extractText(f):
	'generic function which will call appropriate extractor depending on file ext.'
	fileName, ext = os.path.splitext(f.name)
	if ext == '.pdf':
		return extractTextFromPdf(f)
	elif ext == '.doc':
		return extractTextFromDoc(f)
	elif ext == '.txt':
		return extractTextFromTxt(f)
	else:
		return


def extractTextFromPdf(f):
	'uses pyPdf and extracts text from pdf file.'
	# must handle exceptions
	inp = PdfFileReader(file(f, "rb"))
	str = ''
	for each_page in range(inp.getNumPages()):
		str += inp.getPage(each_page).extractText()
	return str		

def extractTextFromDoc(f):
	'''
	MS word files are converted to txt by using antiword program. works for most cases.
	'''
	str = os.popen("antiword "+ f).read()
	# process p
	return str

def extractTextFromTxt(f):
	'plain txt files.'
	#inputf = open(f)
	#str = inputf.read()
	#inputf.close()
	#return str
        return f.read()
