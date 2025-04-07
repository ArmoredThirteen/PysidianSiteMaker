import os
import sys
import shutil

import json

import DirectoryMap
import PageBuilder
import SiteData


# Get arguments
configsDir = sys.argv[1]
vaultDir = sys.argv[2]
buildDir = sys.argv[3]

# Files that were built manually and need copied directly
copyDirect = ["style.css"]


def main():
	configFile = os.path.join(configsDir, "psmconfig.json")
	configs = json.loads(open(configFile).read())
	
	siteData = SiteData.SiteData(vaultDir)
	basePagePath = os.path.join(configsDir, configs["basePage"])
	tagsPagePath = os.path.join(configsDir, configs["tagsPage"])
	
	# Clean build directory
	if os.path.isdir(buildDir):
		shutil.rmtree(buildDir)
	
	# Make target root directory
	os.makedirs(buildDir)
	
	# Copy styles directory
	stylesDirFrom = os.path.join(configsDir, configs["stylesDir"])
	stylesDirTo = os.path.join(buildDir, configs["stylesDir"])
	shutil.copytree(stylesDirFrom, stylesDirTo)
	
	#defaultStyle = os.sep + os.path.normpath(configs["styles"]["default"])
	siteData.defaultStyleLoc = os.sep + os.path.normpath(configs["styles"]["default"])
	
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


def IsMDFile(filename):
	return filename[-3:] == ".md"


if __name__ == '__main__':
	main()
