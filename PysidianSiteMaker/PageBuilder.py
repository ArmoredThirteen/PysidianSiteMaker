import os
import re
import string

import markdown


def GetPageText(basePagePath, targetPath, siteData, bodySourcePath, file):
	basePage = open(basePagePath).read()
	bodyText = open(bodySourcePath).read()
	
	# For whatever reason, this find/replace has to go before the tag find/replace
	# Otherwise links found later in the same line of a tag don't get found properly and aren't replaced
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
	pattern = "#[^\s#][^\s" + string.punctuation + "#]*"
	tags = list(set(re.findall(pattern, bodyText)))
	for tag in tags:
		siteData.AddTag(tag, file)
		markdownLink = siteData.GetTagAsLink(tag)
		#print(tag + ": " + markdownLink)
		bodyText = bodyText.replace(tag, markdownLink)
	
	# Convert body from markdown to html
	bodyText = markdown.markdown(bodyText)
	
	# Format replace body content and the css style location
	page = basePage.format(bodyContents = bodyText, styleLocation = siteData.defaultStyleLoc)
	return page


def BuildPage(basePagePath, siteData, file, vaultDir, buildDir):
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
	pageText = GetPageText(basePagePath, targetPath, siteData, sourcePath, file)
	
	# Write to target file
	with open(targetPath, 'w') as f:
		f.write(pageText)


#TODO This method, and likely some of the tag logic surrounding it, is totally fucked
def BuildTagPage(tagPagePath, siteData, tag, tagsDir, buildDir):
	tagPageText = open(tagPagePath).read()
	
	tagName = tag[1:]
	tagPage = tagName + ".html"
	targetPath = os.path.join(buildDir, tagsDir, tagPage)
	
	# Page text is a list of pages with the tag
	bodyText = ""
	for tagPage in siteData.tags[tag]:
		bodyText += "- " + siteData.dirMap.GetFileAsLink(tagPage) + os.linesep
	
	bodyText = markdown.markdown(bodyText)
	
	page = tagPageText.format(bodyContents=bodyText, styleLocation=siteData.defaultStyleLoc)
	
	# Write to target file
	with open(targetPath, 'w') as f:
		f.write(page)
	