fondz 
-----

[![travis-ci status](https://travis-ci.org/edsu/fondz.png)](http://travis-ci.org/edsu/fondz)

fondz is a tool for auto-generating an "archival description" for born
digital content found in a [bag](http://en.wikipedia.org/wiki/BagIt) or series 
of bags. This description is expressed as static HTML, suitable for viewing in 
both online and offline mode. The assumption is that we'll be able to read HTML 
in browsers for some time to come (hopefully), so it is a logical long term
preservation format.

While fondz's output is simple, and easy to preserve, it is generated
using some hideously complex, but nevertheless, rather useful pieces of 
opensource software:

* [libreoffice](http://www.libreoffice.org/) - for converting various document formats to html
* [mallet](http://mallet.cs.umass.edu/) - for creating topic models of textual content
* [file/libmagic](http://www.darwinsys.com/file/) - the venerable unix file identification utility
* [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/) - for extracting image metadata

As better opensource tools for converting documents and summarizing their 
contents become available they can be swapped out for the ones we're using 
now.

Thanks go to Twitter and Facebook for their HTML based archive packages, and
to [Jekyll](http://jekyllrb.com/) and other static site generators, which 
were an inspiration for fondz.

Example
-------

Here's an example for generating a finding aid for two bags, the first bag 
which contains a Word document `abc.doc`, and the second which contains a 
WordPerfect document `def.wpd`.

    % fondz example /path/to/a/bag /path/to/another/bag
    % tree example/
    example/
    ├── css
    │   └── style.css
    ├── derivatives
    │   └── html
    │       ├── 1
    │       │   └── abc.html
    │       └── 2
    │           └── def.html
    ├── index.html
    ├── js
    │   └── topics.json
    └── originals
        ├── 1 -> /path/to/a/bag
        └── 2 -> /path/to/another/bag

Once fondz has run you should be able to open `index.html` in your 
browser and browse the content.

Install
-------

These instructions assume you are on Ubuntu. You should be able to adapt them
for other systems. We need to build the latest Mallet because it has some fixes
that aren't available in the last release (v2.0.7):

* sudo apt-get install libreoffice-dev python-pip mercurial default-jdk ant libimage-exiftool-perl unoconv
* hg clone http://hg-iesl.cs.umass.edu/hg/mallet
* cd mallet ; ant ; cd .. ; sudo mv mallet /opt
* add /opt/mallet/bin to your $PATH
* sudo pip install fondz

Ideas
-----

These are ideas that seem theoretically doable. If you have similar
ideas to add, please send me a pull request for your changes to the README.md, 
or open an issue here on Github.

* list of bags, their contents, checksums and bag-info.txt metadata
* file format report, including a summary for the entire collection
* pii report w/ bulk extractor?
* topic models for textual content
* convert document formats to HTML/pdf for viewing
* extract image metadata with exiftool
* provide gallery views of extracted images
* zoomable interface for large images using leaflet + generated dzi files?
  e.g. http://content.wdl.org/1/service/dzi/1/1.dzi
* ocr image files with tesseract, and save off hocr output for topic modeling
  etc.
* unpack mbox files into messages that can be topic modeled and displayed, 
  network graphs of email correspondence?
* send html output through WikipediaMiner to try to get links to Wikipedia
  summarize entities found, get metadata for them from dbpedia, freebase, etc.
* do named entity recognition with Stanford NER, or something similar.
* a tool that can summarize/index a collection of fondz descriptions
* libreoffice/unoconv pool/queue for converting lots of documents in parallel

Notes
-----

If you are on OSX and want to convince fondz to use your OpenOffice install put
a script like this named `libreoffice` in your PATH:

    #!/bin/sh

    cd /Applications/LibreOffice.app/Contents/MacOS/
    ./soffice $@

License
-------

* CC0
