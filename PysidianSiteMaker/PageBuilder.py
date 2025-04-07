import os
import re

import markdown


def GetPageText(basePagePath, siteData, bodySourcePath, styleFileName):
	basePage = open(basePagePath).read()
	bodyText = open(bodySourcePath).read()
	
	# Find and replace Obsidian's double bracket links to be links to html pages
	pattern = "\[+.*?]]"
	links = list(set(re.findall(pattern, bodyText)))
	for link in links:
		linkName = link[2:-2] + ".md"
		if not siteData.dirMap.HasFile(linkName):
			continue
		
		markdownLink = siteData.dirMap.GetFileAsLink(linkName)
		bodyText = bodyText.replace(link, markdownLink)
	
	# Find and replace tags and record them in the site data
	pattern = "#[^\s#][^\s#]*"
	tags = list(set(re.findall(pattern, bodyText)))
	for tag in tags:
		siteData.AddTag(tag)
		markdownLink = siteData.GetTagAsLink(tag)
		bodyText = bodyText.replace(tag, markdownLink)
	
	# Convert body from markdown to html
	bodyText = markdown.markdown(bodyText)
	
	# Format replace body content and the css style location
	page = basePage.format(bodyContents = bodyText, styleLocation = styleFileName)
	return page


def BuildPage(basePagePath, siteData, file, vaultDir, buildDir, styleFileName):
	localDir = siteData.dirMap.GetFileDir(file)
	
	# Source values
	localSourcePath = siteData.dirMap.GetFilePath(file)
	sourcePath = os.path.join(vaultDir, localSourcePath)
	
	# Target values
	localTargetPath = localSourcePath[:-3] + ".html"
	targetPath = os.path.join(buildDir, localTargetPath)
	
	# Make target directory
	os.makedirs(os.path.join(buildDir, localDir), exist_ok=True)
	
	# Build page text
	pageText = GetPageText(basePagePath, siteData, sourcePath, styleFileName)
	
	# Write to target file
	with open(targetPath, 'w') as f:
		f.write(pageText)
