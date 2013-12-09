diagnidnif
----------

diagnidnif, or "finding aid" backwards, is a tool for auto-generating an 
"archival" description of data found in a [bag](http://en.wikipedia.org/wiki/BagIt), or a series of bags. This description is expressed as static HTML, for 
viewing offline. The implicit assumption is that we'll be able to read HTML 
in browsers for some time to come, hopefully right?

While diagnidnif's output is simple, and easy to preserve, it is a wrapper 
around some hideously complex, but rather useful pieces of software:

* libreoffice for converting various document formats
* mallet for creating topic models of textual content

As better opensource tools for converting documents and summarizing their 
contents come on the scene they can be swapped out.

Example
-------

Here's an example for generating a finding aid for two bags, the first bag 
which contains a Word document `abc.doc`, and the second which contains a 
WordPerfect document `def.wpd`.

    % diagnidnif example /path/to/a/bag /path/to/another/bag
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

Install
-------

These instructions assume you are on Ubuntu. You should be able to adapt them
for other systems. We need to build the latest Mallet because it has some fixes
that aren't available in the last release (v2.0.7):

* sudo apt-get install libreoffice-dev python-pip mercurial default-jdk ant
* hg clone http://hg-iesl.cs.umass.edu/hg/mallet
* cd mallet ; ant ; cd .. ; sudo mv mallet /opt
* add /opt/mallet/bin to your $PATH
* sudo pip install diagnidnif

License
-------

* CC0
