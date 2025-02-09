import os
import sys
import shutil

import DirectoryMap
import PageBuilder


# Get arguments
vaultDir = sys.argv[1]

# Files that were built manually and need copied directly
copyDirect = ["style.css"]


def main():
	dirMap = DirectoryMap.DirectoryMap(vaultDir)
	
	sourceDir = vaultDir
	targetDir = vaultDir + "_build"
	
	basePagePath = os.path.join(sourceDir, "basePage.html")
	
	# Clean build directory
	if os.path.isdir(targetDir):
		shutil.rmtree(targetDir)
	
	# Make target root directory
	os.makedirs(targetDir)
	
	# Copy manually built files
	for i in range(len(copyDirect)):
		copyFrom = os.path.join(sourceDir, copyDirect[i])
		copyTo = os.path.join(targetDir, copyDirect[i])
		shutil.copy2(copyFrom, copyTo)
	
	# Build and write all relevant files
	for file in dirMap.map:
		# Only worried about md files for now
		if not IsMDFile(file):
			continue
		
		#basePagePath, dirMap, file, sourceDir, targetDir, styleFileName
		PageBuilder.BuildPage(basePagePath, dirMap, file, sourceDir, targetDir, "style.css")


def IsMDFile(filename):
	return filename[-3:] == ".md"


if __name__ == '__main__':
	main()
