import markdown


def GetBody(bodySourceFile):
	return open(bodySourceFile).read()


def BuildPage(headerFile, bodySourceFile, footerFile, target):
	header = open(headerFile).read()
	bodySource = open(bodySourceFile).read()
	body = markdown.markdown(bodySource)
	footer = open(footerFile).read()
	
	with open(target, 'w') as f:
		f.write(header)
		f.write(body)
		f.write(footer)
