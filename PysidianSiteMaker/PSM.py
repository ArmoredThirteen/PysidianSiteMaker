import os
import sys
import shutil

import DirectoryMap
import PageBuilder


# Get arguments
vaultDir = sys.argv[1]


def main():
	dirMap = DirectoryMap.DirectoryMap(vaultDir)
	
	sourceDir = vaultDir
	targetDir = vaultDir + "_build"
	
	headerFile = sourceDir + "/header.html"
	footerFile = sourceDir + "/footer.html"
	
	# Clean build directory
	if os.path.isdir(targetDir):
		shutil.rmtree(targetDir)
	
	# Make target root directory
	os.makedirs(targetDir)
	
	# Copy over manually built files
	toCopy = ["/style.css"]
	for i in range(len(toCopy)):
		sourceFile = sourceDir + toCopy[i]
		targetFile = targetDir + toCopy[i]
		shutil.copy2(sourceFile, targetFile)
	
	# Build and write all found files
	for file in dirMap.map:
		if not IsMDFile(file):
			continue
		
		# Make target directory
		os.makedirs(os.path.join(targetDir, dirMap.GetFileDir(file)), exist_ok=True)
		
		# Gather path info for source and target files
		localFilePath = dirMap.GetFilePath(file)
		sourcePath = os.path.join(sourceDir, localFilePath)
		targetPath = os.path.join(targetDir, localFilePath)[:-3] + ".html"
		
		#sys.stdout.write("Source: " + sourcePath + "\n")
		#sys.stdout.write("Target: " + targetPath + "\n")
		
		# Build the html page
		PageBuilder.BuildPage(headerFile, sourcePath, footerFile, targetPath)


def IsMDFile(filename):
	return filename[-3:] == ".md"


if __name__ == '__main__':
	main()
