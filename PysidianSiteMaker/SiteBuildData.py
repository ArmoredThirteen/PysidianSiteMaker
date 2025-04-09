import json
import os


class SiteBuildData:
	"""Stores data relevant for building the website from a vault."""
	
	configsAbsDir = ""
	vaultAbsDir = ""
	buildAbsDir = ""
	
	tagsLocalDir = ""
	
	configs = {}
	
	notePageTemplateText = ""
	tagPageTemplateText = ""
	
	defaultStyleLoc = ""
	
	pages = {} # key:val == pageName:pageLocalDir
	tags = {} # key:val == tagName:[pageName, ...]
	
	
	def __init__(self, configsAbsDir, vaultAbsDir, buildAbsDir):
		# JSON configuration settings
		configFile = os.path.join(configsAbsDir, "psmconfig.json")
		configs = json.loads(open(configFile).read())
		
		# Page template files
		templatesConfigs = configs["pageTemplates"]
		templatesAbsDir = os.path.join(configsAbsDir, templatesConfigs["dir"])
		notePageTemplateFile = os.path.join(templatesAbsDir, templatesConfigs["note"])
		tagPageTemplateFile = os.path.join(templatesAbsDir, templatesConfigs["tag"])
		
		# CSS files
		cssConfigs = configs["CSS"]
		cssLocalDir = cssConfigs["dir"]
		defaultStyleLoc = os.path.join(cssLocalDir, cssConfigs["default"])
		
		self.configsAbsDir = configsAbsDir
		self.vaultAbsDir = vaultAbsDir
		self.buildAbsDir = buildAbsDir
		self.tagsLocalDir = configs["TagsLocalDir"]
		self.configs = configs
		self.notePageTemplateText = open(notePageTemplateFile).read()
		self.tagPageTemplateText = open(tagPageTemplateFile).read()
		self.defaultStyleLoc = os.sep + defaultStyleLoc
	
	
	def AddPage(self, pageName, pageLocalDir):
		self.pages[pageName] = pageLocalDir
	
	
	def AddTag(self, tagName, pageName):
		if tagName not in self.tags:
			self.tags[tagName] = []
		
		self.tags[tagName].append(pageName)
	
	
	def GetPageLocalLoc(self, pageName):
		return os.path.join(self.pages[pageName], pageName)
	
	def GetPageAsMarkdownLink(self, pageName):
		filePath = self.GetPageLocalLoc(pageName)
		return f"[{pageName[:-3]}]({os.sep}{filePath[:-3]}.html)"
	
	
	def GetTagPages(self, tagName):
		return self.tags[tagName]
	
	def GetTagAsMarkdownLink(self, tagName):
		return f"[{tagName}]({os.sep}Tags{os.sep}{tagName[1:]}.html)"
	
	
	def HasPage(self, page):
		return page in self.pages
	
	
	def __str__(self):
		return (f"== SiteBuildData:{os.linesep}"
				f"   - configsAbsDir =   '{self.configsAbsDir}',{os.linesep}"
				f"   - vaultAbsDir =     '{self.vaultAbsDir}',{os.linesep}"
				f"   - buildAbsDir =     '{self.buildAbsDir}',{os.linesep}"
				f"   - defaultStyleLoc = '{self.defaultStyleLoc}'")