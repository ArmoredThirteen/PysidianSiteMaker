import os
import re

import markdown


def GetPageText(basePagePath, dirMap, bodySourcePath, styleFileName):
	basePage = open(basePagePath).read()
	bodyText = open(bodySourcePath).read()
	
	# Find and replace Obsidian's double bracket links to be links to html pages
	pattern = "\[+.*?]]"
	links = list(set(re.findall(pattern, bodyText)))
	for link in links:
		linkName = link[2:-2] + ".md"
		if not dirMap.HasFile(linkName):
			continue
		
		markdownLink = dirMap.GetFileAsLink(linkName)
		bodyText = bodyText.replace(link, markdownLink)
	
	# Convert body from markdown to html
	bodyText = markdown.markdown(bodyText)
	
	# Format replace body content and the css style location
	page = basePage.format(bodyContents = bodyText, styleLocation = styleFileName)
	return page


def BuildPage(basePagePath, dirMap, file, vaultDir, buildDir, styleFileName):
	localDir = dirMap.GetFileDir(file)
	
	# Source values
	localSourcePath = dirMap.GetFilePath(file)
	sourcePath = os.path.join(vaultDir, localSourcePath)
	
	# Target values
	localTargetPath = localSourcePath[:-3] + ".html"
	targetPath = os.path.join(buildDir, localTargetPath)
	
	# Make target directory
	os.makedirs(os.path.join(buildDir, localDir), exist_ok=True)
	
	# Build page text
	pageText = GetPageText(basePagePath, dirMap, sourcePath, styleFileName)
	
	# Write to target file
	with open(targetPath, 'w') as f:
		f.write(pageText)
