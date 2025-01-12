import sys
import os
import shutil

import PageBuilder


# Get arguments
vaultDir = sys.argv[1]


def main():
	sourceDir = vaultDir
	targetDir = vaultDir + "_build"
	
	# Clean build directory
	if os.path.isdir(targetDir):
		shutil.rmtree(targetDir)
	os.makedirs(targetDir)
	
	# Build single test page from the targetDir argument
	headerFile = sourceDir + "/header.html"
	bodySourceFile = sourceDir + "/index.md"
	footerFile = sourceDir + "/footer.html"
	target = targetDir + "/index.html"
	PageBuilder.BuildPage(headerFile, bodySourceFile, footerFile, target)
	
	# Copy over manually built files
	toCopy = ["/style.css"]
	for i in range(len(toCopy)):
		sourceFile = sourceDir + toCopy[i]
		targetDir = targetDir + toCopy[i]
		shutil.copy2(sourceFile, targetDir)


if __name__ == '__main__':
	main()
