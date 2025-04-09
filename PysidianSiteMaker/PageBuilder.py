import os
import re
import string

import markdown


def ProcessNotePage(siteBuildData, page):
	# All note pages are .md
	if page[-3:] != ".md":
		return
	
	pageFile = os.path.join(siteBuildData.vaultAbsDir, siteBuildData.GetPageLocalLoc(page))
	pageText = open(pageFile).read()
	
	# Replace all the [[page]] links with [page](localPath)
	linkPattern = "\[+.*?]]"
	links = list(set(re.findall(linkPattern, pageText)))
	for link in links:
		linkName = link[2:-2] + ".md"
		if not siteBuildData.HasPage(linkName):
			continue
		
		markdownLink = siteBuildData.GetPageAsMarkdownLink(linkName)
		pageText = pageText.replace(link, markdownLink)
	
	# Replace all the #tag with [#tag](localTagPath)
	tagPattern = "#[^\s#][^\s" + string.punctuation + "#]*"
	tags = list(set(re.findall(tagPattern, pageText)))
	for tag in tags:
		siteBuildData.AddTag(tag, page)
		markdownLink = siteBuildData.GetTagAsMarkdownLink(tag)
		pageText = pageText.replace(tag, markdownLink)
	
	# Get the mainHeading title of the page
	mainHeading = page[:-3]
	if page == siteBuildData.configs["indexPage"]["baseFile"]:
		mainHeading = siteBuildData.configs["indexPage"]["mainHeading"]
	
	# Convert markdown to html
	pageText = markdown.markdown(pageText)
	htmlText = siteBuildData.notePageTemplateText.format(
		styleLocation   = siteBuildData.defaultStyleLoc,
		faviconLocation = siteBuildData.faviconLoc,
		mainHeading     = mainHeading,
		bodyContents    = pageText)
	
	# Write to new html file
	targetFile = os.path.join(siteBuildData.buildAbsDir, siteBuildData.GetPageLocalLoc(page))[:-3] + ".html"
	with open(targetFile, 'w') as f:
		f.write(htmlText)


def BuildTagPage(siteBuildData, tag):
	# Make markdown list of pages with given tag
	pageText = ""
	for tagPage in siteBuildData.tags[tag]:
		pageText += f"- {siteBuildData.GetPageAsMarkdownLink(tagPage)}{os.linesep}"
	
	# Convert markdown to html
	pageText = markdown.markdown(pageText)
	htmlText = siteBuildData.tagPageTemplateText.format(
		styleLocation   = siteBuildData.defaultStyleLoc,
		faviconLocation = siteBuildData.faviconLoc,
		mainHeading     = tag[1:],
		bodyContents    = pageText)
	
	# Write to new html file
	targetFile = os.path.join(siteBuildData.buildAbsDir, siteBuildData.tagsLocalDir, f"{tag[1:]}.html")
	with open(targetFile, 'w') as f:
		f.write(htmlText)