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

    source = sourceDir + "/index.md"
    target = targetDir + "/index.html"
    PageBuilder.BuildPage(source, target)


if __name__ == '__main__':
    main()