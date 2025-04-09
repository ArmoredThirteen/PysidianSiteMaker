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
	
	# Folders that need fully copied
	CopyFolder(siteBuildData, siteBuildData.configs["CSS"]["dir"])
	CopyFolder(siteBuildData, siteBuildData.configs["images"]["dir"])
	
	# Make new dir for every page
	for pageLocalDir in siteBuildData.pages.values():
		os.makedirs(os.path.join(siteBuildData.buildAbsDir, pageLocalDir), exist_ok=True)
	
	# Make Tags dir
	os.makedirs(os.path.join(siteBuildData.buildAbsDir, siteBuildData.tagsLocalDir), exist_ok=True)


def CopyFolder(siteBuildData, localDir):
	dirFrom = os.path.join(siteBuildData.configsAbsDir, localDir)
	dirTo = os.path.join(siteBuildData.buildAbsDir, localDir)
	shutil.copytree(dirFrom, dirTo)


if __name__ == '__main__':
	main()
