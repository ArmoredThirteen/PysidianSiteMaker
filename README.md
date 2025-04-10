# ObsidianSiteMaker
Python tool for turning Obsidian projects into HTML pages

## Using PSM.py
### python PSM.py <configsDir> <vaultDir> <buildDir> <optional:siteDir>
- configsDir: The directory to find psmconfig.json in. See the /PSMConfigs folder for an example.
- vaultDir: Root directory of the obsidian vault to convert.
- buildDir: Where to send the resulting built files. If it exists already it will be wiped clean, if it does not exist it will be made automatically.
- siteDir: This can optionally be used if the site will be hosted in a subfolder. For instance if you're hosting multiple sites in one domain. This prepends to various links as needed (such as linking to another page within the site or the favicon.ico location).

## psmconfig.json
- pageTemplates
	- dir: Directory housing template pages
	- note: Described below, the html used as the base of a Note Page
	- tag: Described below, the html used as the base of a Tag Page
- css
	- dir: Directory housing css files
	- default: Default css file used across the site
- images
	- dir: Directory housing common image files
	- favicon: Default favicon.ico file used across the site
- tagsLocalDir: When generating Tag Pages, they get stored in this directory
- indexPage
	- baseFile: Location of the index.md file. Used to indicate which page to use the mainHeading with
	- mainHeading: Used as the heading to replace the baseFile's heading. Basically it is to prevent the index.html page from having **index** at the top looking all dumb
- headTitle: Used for page header titles

## Page Templates
PSM uses html page templates. They house data that would not be included when converting an md file, such as common header or footer code. They have variables encased in squiggle brackets {} which PSM uses to add in page contents.
### Note Page
The standard page used to store a converted vault's md file as the body.
- headTitle: The page's title, from the baseTitle config above
- styleLocation: Where to find the css style
- faviconLocation: Where to find the favicon.ico
- mainHeading: Page title
- bodyContents: Holds the contents of the converted md file
### Tag Page
Tags found in other pages are linked to a tag page. These in turn can list all pages using that tag. Variables are the same as in a Note Page but the bodyContents is a generated list of links to pages that use the given tag, instead of a converted md file found in the vault.