#TODO Needs a better name, "Data" is famously non-descriptive
import os
from collections import defaultdict

import DirectoryMap


class SiteData:
	"""Used for storing persistent information about the website. Things like the directory map or list of tags"""
	
	defaultStyleLoc = ""
	tags = defaultdict(list)
	dirMap = None
	
	
	def __init__(self, rootDir):
		self.dirMap = DirectoryMap.DirectoryMap(rootDir)
		
		
	def AddTag(self, tag, targetPagePath):
		#print("Adding " + str(tag) + " for " + str(targetPagePath))
		self.tags[tag].append(targetPagePath)
	
	
	def GetTagAsLink(self, tag):
		tagPath = os.sep + "Tags" + os.sep + tag[1:]
		return "[" + tag + "](" + tagPath + ".html)"