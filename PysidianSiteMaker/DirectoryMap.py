import os
import sys


class DirectoryMap:
	"""Creates a map of files within a given directory. Recursively searches subfolders for files."""
	
	
	map = {}
	
	
	def __init__(self, rootDir):
		self.BuildMap(rootDir, '', '')
	
	
	def BuildMap(self, currDir, localDir, indent):
		items = os.listdir(currDir)
		for item in items:
			# Skip obsidian's config folder
			if item == ".obsidian":
				continue
			
			currPath = os.path.join(currDir, item)
			localPath = os.path.join(localDir, item)
			
			# Add file to self.map
			if os.path.isfile(currPath):
				#sys.stdout.write(indent + '- ' + item + '\n')
				if self.HasFile(item):
					sys.stdout.write("Duplicate file name: " + item + '\n')
				self.map[item] = localDir
			
			# Continue down folder structure
			elif os.path.isdir(currPath):
				#sys.stdout.write((indent + '+ ' + item + '\n'))
				self.BuildMap(currPath, localPath, indent + '  ')
	
	
	def HasFile(self, fileName):
		return fileName in self.map
	
	
	def GetFileDir(self, fileName):
		return self.map[fileName]
	
	
	def GetFilePath(self, fileName):
		return os.path.join(self.map[fileName], fileName)
	
	
	def GetFileAsLink(self, fileName):
		# Convert "[[FileName.md]]" into "[FileName](/Subfolder/FileName.html)"
		filePath = os.sep + str(self.GetFilePath(fileName))
		return "[" + fileName[:-3] + "](" + filePath[:-3] + ".html)"
	