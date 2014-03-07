#Indonesian Law Documents Linking Project

This is a small project to download collections of Indonesian law documents, then parse and annotate links between the documents.

##Directory
```
/
|--- build             currently contains list of html documents
|--- logs              list of my logfile
+--- tmp               just a place for working
```

##Requirements
Some scripts in this project will need
- Python 2.7
- PhantomJS 1.4.0

##Steps
So far steps I have made

```
$#This will download files from www.djpp.kemenkumham.go.id
$./downloader.js

$#This will move the documents for rendering
$cp downloads/data-* tmp/renderinput

$#Since most the HTML files use Javascript obfuscation, this will render the final HTML result using PhantomJS
$./render.js tmp/renderinput build/renderoutput

$#This will remove unused HTML tags and output renamed files
$./clean_html.python tmp/renderoutput tmp/cleaned

$#So far
$cp tmp/cleaned build

$#Restructuring the HTML to make it easier to diff
$for f in `find build/ -type f`; do   echo $f;   tidy -i -f tmp/$f -o $f $f; done

```

##Changelog
2014.02.27 

- Started the project

2014.03.01 

- Renaming the files to a more uniform structure
- Tidying the HTML content
- NOTE: There are several instance where the file name doesn't reflect the real document number. For example, when I do a diff between file ps8-2012bt.html and ps8-2012.html I found that the real document number for the latter is 16-2013. There is still no clear insight from the documents about what the 'bt' means. 
- NOTE: The documents that have suffix 'pjl', e.g. `pp42-2013pjl.html`, are documents that contain explanation about the counterpart.
- NOTE: PBI documents has three numbering parts, instead of two like others.
- NOTE: There is one KEPPRES instance that has 'M' in the title: KEPPRES 162/M 2000

2014.03.07

- Changing some div that only has children tags to ol/li tag.