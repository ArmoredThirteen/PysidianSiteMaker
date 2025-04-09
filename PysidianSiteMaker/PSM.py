import os
import sys
import shutil

import PageBuilder
from SiteBuildData import SiteBuildData


def main():
	# CLI arguments
	configsAbsDir = sys.argv[1]
	vaultAbsDir = sys.argv[2]
	buildAbsDir = sys.argv[3]
	
	# The build data to be passed to various systems
	siteBuildData = SiteBuildData(configsAbsDir, vaultAbsDir, buildAbsDir)
	ScanVault(siteBuildData, vaultAbsDir, '')
	
	RemakeBuildDir(siteBuildData)
	
	for page in siteBuildData.pages:
		PageBuilder.ProcessNotePage(siteBuildData, page)
	
	for tag in siteBuildData.tags:
		PageBuilder.BuildTagPage(siteBuildData, tag)


def ScanVault(siteBuildData, currDir, localDir):
	items = os.listdir(currDir)
	for item in items:
		# Skip obsidian's config folder
		if item == ".obsidian":
			continue
		
		currPath = os.path.join(currDir, item)
		localPath = os.path.join(localDir, item)
		
		# Continue down folder structure
		if os.path.isdir(currPath):
			ScanVault(siteBuildData, currPath, localPath)
			continue
		
		# Add file to pages
		if siteBuildData.HasPage(item):
			print(f"Duplicate file name: {item}")
		siteBuildData.pages[item] = localDir


def RemakeBuildDir(siteBuildData):
	# Reset build directory
	if os.path.isdir(siteBuildData.buildAbsDir):
		shutil.rmtree(siteBuildData.buildAbsDir)
	os.makedirs(siteBuildData.buildAbsDir)
	
	# Copy CSS folder
	cssLocalDir = siteBuildData.configs["CSS"]["dir"]
	cssDirFrom = os.path.join(siteBuildData.configsAbsDir, cssLocalDir)
	cssDirTo = os.path.join(siteBuildData.buildAbsDir, cssLocalDir)
	shutil.copytree(cssDirFrom, cssDirTo)
	
	# Make new dir for every page
	for pageLocalDir in siteBuildData.pages.values():
		os.makedirs(os.path.join(siteBuildData.buildAbsDir, pageLocalDir), exist_ok=True)
	
	# Make Tags dir
	os.makedirs(os.path.join(siteBuildData.buildAbsDir, siteBuildData.tagsLocalDir), exist_ok=True)


'''
def main():
	# Build and write main md files as html
	for file in siteData.dirMap.map:
		# Only worried about md files for now
		if not IsMDFile(file):
			continue
		
		PageBuilder.BuildPage(basePagePath, siteData, file, vaultDir, buildDir)
	
	# Add tag pages in
	tagsDir = os.path.join(buildDir, "Tags")
	os.makedirs(tagsDir, exist_ok=True)
	for tag in siteData.tags:
		#print(tag)
		PageBuilder.BuildTagPage(tagsPagePath, siteData, tag, tagsDir, buildDir)
'''

def IsMDFile(filename):
	return filename[-3:] == ".md"


if __name__ == '__main__':
	main()
