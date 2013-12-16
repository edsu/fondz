fondz 
-----

[![travis-ci status](https://travis-ci.org/edsu/fondz.png)](http://travis-ci.org/edsu/fondz)

fondz is a tool for auto-generating an "archival description" for born
digital content found in a [bag](http://en.wikipedia.org/wiki/BagIt) or series 
of bags. This description is expressed as static HTML, for viewing in both 
online and offline mode. The assumption is that we'll be able to read HTML 
in browsers for some time to come (hopefully), so it is a logical preservation 
format. 

While fondz's output is simple, and easy to preserve, it is generated
using some hideously complex, but nevertheless, rather useful pieces of 
software:

* [libreoffice](http://www.libreoffice.org/) for converting various document formats to text and html
* [mallet](http://mallet.cs.umass.edu/) for creating topic models of textual content

As better opensource tools for converting documents and summarizing their 
contents become available they can be swapped out for the ones we're using 
now.

Thanks go to Twitter and Facebook for their HTML based archive packages which
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

* sudo apt-get install libreoffice-dev python-pip mercurial default-jdk ant
* hg clone http://hg-iesl.cs.umass.edu/hg/mallet
* cd mallet ; ant ; cd .. ; sudo mv mallet /opt
* add /opt/mallet/bin to your $PATH
* sudo pip install fondz

Ideas
-----

* list of bags and bag metadata
* inventory of files
* file format report
* pii report?
* topic models for textual content
* convert document formats to HTML/pdf for viewing
* unpack mbox files into messages that can be topic modeled and displayed
* provide gallery views of extracted images, try to extract image metadata
* a tool that can summarize a collection of fondz descriptions

License
-------

* CC0
