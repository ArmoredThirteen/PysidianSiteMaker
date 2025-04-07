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
	
	# Clean build directory
	if os.path.isdir(buildDir):
		shutil.rmtree(buildDir)
	
	# Make target root directory
	os.makedirs(buildDir)
	
	# Copy styles directory
	#styleFrom = os.path.abspath(os.path.join(configsDir, configs["styles"]["default"]))
	#styleTo = os.path.join(buildDir, "style.css")
	#shutil.copy2(styleFrom, styleTo)
	stylesDirFrom = os.path.join(configsDir, configs["stylesDir"])
	stylesDirTo = os.path.join(buildDir, configs["stylesDir"])
	shutil.copytree(stylesDirFrom, stylesDirTo)
	
	defaultStyle = os.sep + os.path.normpath(configs["styles"]["default"])
	print(defaultStyle)
	
	# Build and write all relevant files
	for file in siteData.dirMap.map:
		# Only worried about md files for now
		if not IsMDFile(file):
			continue
		
		#basePagePath, dirMap, file, sourceDir, targetDir, styleFileName
		PageBuilder.BuildPage(basePagePath, siteData, file, vaultDir, buildDir, defaultStyle)


def IsMDFile(filename):
	return filename[-3:] == ".md"


if __name__ == '__main__':
	main()
