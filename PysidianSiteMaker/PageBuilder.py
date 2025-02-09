import os

import markdown


def GetPageText(basePagePath, bodySourcePath, styleLocation):
	basePage = open(basePagePath).read()
	bodySource = open(bodySourcePath).read()
	body = markdown.markdown(bodySource)
	
	page = basePage.format(bodyContents = body, styleLocation = styleLocation)
	return page


def BuildPage(basePagePath, dirMap, file, sourceDir, targetDir, styleFileName):
	localDir = dirMap.GetFileDir(file)
	
	# Source values
	localSourcePath = dirMap.GetFilePath(file)
	sourcePath = os.path.join(sourceDir, localSourcePath)
	
	# Target values
	localTargetPath = localSourcePath[:-3] + ".html"
	targetPath = os.path.join(targetDir, localTargetPath)
	
	# Style file location
	folderDepth = localSourcePath.count(os.sep)
	styleLocation = ((".." + os.sep) * folderDepth) + styleFileName
	
	# Make target directory
	os.makedirs(os.path.join(targetDir, localDir), exist_ok=True)
	
	# Build the html page
	pageText = GetPageText(basePagePath, sourcePath, styleLocation)
	with open(targetPath, 'w') as f:
		f.write(pageText)
