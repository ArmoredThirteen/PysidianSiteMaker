#TODO Needs a better name, "Data" is famously non-descriptive
import os

import DirectoryMap


class SiteData:
	"""Used for storing persistent information about the website. Things like the directory map or list of tags"""
	
	tags = []
	dirMap = None
	
	
	def __init__(self, rootDir):
		self.dirMap = DirectoryMap.DirectoryMap(rootDir)
		
		
	def AddTag(self, tagName):
		if tagName in self.tags:
			return
		
		self.tags.append(tagName)
		
	def GetTagAsLink(self, tag):
		tagPath = os.sep + "Tags" + os.sep + tag[1:]
		return "[" + tag + "](" + tagPath + ")"