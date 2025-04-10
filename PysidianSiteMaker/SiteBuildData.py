import json
import os


class SiteBuildData:
	"""Stores data relevant for building the website from a vault."""
	
	configsAbsDir = ""
	vaultAbsDir = ""
	buildAbsDir = ""
	siteDir = ""
	
	tagsLocalDir = ""
	
	configs = {}
	
	notePageTemplateText = ""
	tagPageTemplateText = ""
	
	defaultStyleLoc = ""
	faviconLoc = ""
	
	pages = {} # key:val == pageName:pageLocalDir
	tags = {} # key:val == tagName:[pageName, ...]
	
	
	def __init__(self, configsAbsDir, vaultAbsDir, buildAbsDir, siteDir):
		self.configsAbsDir = configsAbsDir
		self.vaultAbsDir = vaultAbsDir
		self.buildAbsDir = buildAbsDir
		self.siteDir = siteDir
		
		# JSON configuration settings
		configFile = os.path.join(configsAbsDir, "psmconfig.json")
		configs = json.loads(open(configFile).read())
		
		# Page template files
		templatesConfigs = configs["pageTemplates"]
		templatesAbsDir = os.path.join(configsAbsDir, templatesConfigs["dir"])
		notePageTemplateFile = os.path.join(templatesAbsDir, templatesConfigs["note"])
		tagPageTemplateFile = os.path.join(templatesAbsDir, templatesConfigs["tag"])
		
		# CSS and default style
		cssConfigs = configs["CSS"]
		cssLocalDir = cssConfigs["dir"]
		defaultStyleLoc = self.WithSiteDir(os.path.join(cssLocalDir, cssConfigs["default"]))
		
		# Images and favicon
		imgConfigs = configs["images"]
		imgLocalDir = imgConfigs["dir"]
		faviconLoc = self.WithSiteDir(os.path.join(imgLocalDir, imgConfigs["favicon"]))
		
		self.tagsLocalDir = configs["TagsLocalDir"]
		self.configs = configs
		self.notePageTemplateText = open(notePageTemplateFile).read()
		self.tagPageTemplateText = open(tagPageTemplateFile).read()
		self.defaultStyleLoc = os.sep + defaultStyleLoc
		self.faviconLoc = os.sep + faviconLoc
	
	
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
		
		linkText = pageName[:-3]
		linkLoc = self.WithSiteDir(filePath[:-3] + ".html")
		
		return f"[{linkText}]({os.sep}{linkLoc})"
	
	
	def GetTagPages(self, tagName):
		return self.tags[tagName]
	
	def GetTagAsMarkdownLink(self, tagName):
		linkText = tagName
		linkLoc = self.WithSiteDir(os.path.join("Tags", tagName[1:] + ".html"))
		return f"[{linkText}]({os.sep}{linkLoc})"
	
	
	def HasPage(self, page):
		return page in self.pages
	
	def HasSiteDir(self):
		return self.siteDir != ""
	
	
	def WithSiteDir(self, path):
		if self.HasSiteDir():
			return os.path.join(self.siteDir, path)
		return path
	
	
	def __str__(self):
		return (f"== SiteBuildData:{os.linesep}"
				f"   - configsAbsDir   = '{self.configsAbsDir}',{os.linesep}"
				f"   - vaultAbsDir     = '{self.vaultAbsDir}',{os.linesep}"
				f"   - buildAbsDir     = '{self.buildAbsDir}',{os.linesep}"
				f"   - defaultStyleLoc = '{self.defaultStyleLoc}'")