invenstory ![travis-ci status](https://travis-ci.org/edsu/invenstory.png)
-----------

invenstory is a tool for auto-generating an "archival" description for born
digital content found in a [bag](http://en.wikipedia.org/wiki/BagIt) or series 
of bags. This description is expressed as static HTML, for viewing in both 
online and offline mode. The assumption is that we'll be able to read HTML 
in browsers for some time to come (hopefully), so it is a logical preservation 
format. 

While invenstory's output is simple, and easy to preserve, it is generated
using some hideously complex, but nevertheless, rather useful pieces of 
software:

* [libreoffice](http://www.libreoffice.org/) for converting various document formats to text and html
* [mallet](http://mallet.cs.umass.edu/) for creating topic models of textual content

As better opensource tools for converting documents and summarizing their 
contents become available they can be swapped out for the ones we're using 
now.

Thanks go to Twitter and Facebook for their HTML based archive packages which
were an inspiration for invenstory.

Example
-------

Here's an example for generating a finding aid for two bags, the first bag 
which contains a Word document `abc.doc`, and the second which contains a 
WordPerfect document `def.wpd`.

    % invenstory example /path/to/a/bag /path/to/another/bag
    % tree example/
    example/
    ├── css
    │   └── style.css
    ├── derivatives
    │   ├── 1
    │   │   └── data
    │   │       ├── abc.html
    │   │       └── abc.txt
    │   └── 2
    │       └── data
    │           ├── def.html
    │           └── def.txt
    ├── index.html
    ├── js
    │   └── topics.js
    └── originals
        ├── 1 -> /path/to/a/bag
        └── 2 -> /path/to/another/bag

Once invenstory has run you should be able to open `index.html` in your 
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
* sudo pip install invenstory

License
-------

* CC0
