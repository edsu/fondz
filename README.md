fondz 
-----

*WORK IN PROGRESS WARNING*

[![travis-ci status](https://travis-ci.org/edsu/fondz.png)](http://travis-ci.org/edsu/fondz)

fondz is a command line tool for auto-generating an "archival description" for a set of born digital content found in a [bag](http://en.wikipedia.org/wiki/BagIt) or series of bags. The name fondz was borrowed from a [humorous](http://curatememe.tumblr.com/post/28097866834/respect-de-fondz-taking-into-consideration-the) take on the archival principle of [provenance](http://www2.archivists.org/glossary/terms/p/provenance) or respect des fonds. fondz works best if you point it at a collection of content that has some thematic unity, such as a collection associated with an individual, family or organization.

The description that fondz generates is expressed as HTML, suitable for 
viewing in both online and offline mode without the need for running software
other than your Web browser. The HTML also contains structured metadata, so 
that it can be easily processed by other applications. fondz is largely an
integration layer for other tools such as:

* [libreoffice](http://www.libreoffice.org/) - for converting various document formats to html
* [mallet](http://mallet.cs.umass.edu/) - for creating topic models of textual content
* [fido](https://github.com/openplanets/fido) - for identifying file formats using the [Pronom](http://www.nationalarchives.gov.uk/PRONOM/Default.aspx) registry.
* [file/libmagic](http://www.darwinsys.com/file/) - the venerable unix file identification utility
* [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/) - for extracting image metadata

As better opensource tools for converting documents and summarizing their 
contents become available they can be swapped out for the ones that are being 
used now.

Thanks go to Twitter and Facebook for their HTML based archive packages, and
to [Jekyll](http://jekyllrb.com/) and other static site generators, which 
were an inspiration for fondz.

Example
-------

Here's an example for generating a finding aid for two bags, the first bag 
which contains a Word document `abc.doc`, and the second which contains a 
WordPerfect document `def.wpd`.

    % fondz create "Collection Name" example /path/to/a/bag /path/to/another/bag
    % tree example/
    example/
    ├── css
    │   └── style.css
    ├── derivatives
    │   ├── 1
    │   │   └── abc.doc.html
    │   └── 2
    │       └── def.wpd.html
    ├── index.html
    ├── js
    │   │── topics.json
    │   └── formats.json
    └── originals
        ├── 1 -> /path/to/a/bag
        └── 2 -> /path/to/another/bag

Once fondz has run you should be able to open `index.html` in your 
browser and browse the content.

Install
-------

On Ubuntu you should be able to install fondz by running `scripts/install`.
If you are on OSX or Windows you should be able to read the install.sh and
figure out what you need to install and put in your PATH.

Ideas
-----

If you've got ideas for things fondz could do, please submit them as
an enhancement issue at [GitHub](https://github.com/edsu/fondz/issues/new).

These are ideas that seem theoretically doable. If you have similar
ideas to add, please send me a pull request for your changes to the README.md, 
or open an issue here on Github.

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
