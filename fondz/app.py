import sys
import clik
import fondz
import logging

from optparse import make_option as opt

version = '0.0.1'
description = "create automated archival descriptions of digital content"
app = clik.App(
    'fondz',
    version=version,
    description=description
)

@app(usage="COLLECTION_NAME COLLECTION_DIR BAG1 [BAG2 ...]",
     opts=(
         opt('-o', 
             '--overwrite', 
             dest='overwrite', 
             action='store_true',
             help='use an existing directory for the fondz project',
             default=False)))

def create(args, opts, console):
    """
    Create a new fondz project.

    Pass in a name for your collection, a directory to use for your fondz 
    project, and the path(s) to one or more bag directories.

        % fondz create "Carl Sagan Collection" /vol/fondz/sagan /vol/bags/bag1 /vol/bags/bag2

    """
    if len(args) < 3:
        console.error("You must supply a fondz directory path and at least one bag.")
        sys.exit(2)
    try:
        fondz.create(*args, overwrite=opts.overwrite)
    except Exception as e:
        console.error(e)


@app(usage="FONDZ_DIR BAG_DIR")
def add_bag(args, console):
    """
    Add a bag to an existing fondz project.

    Pass in the directory for your fondz project, and the path to one or 
    more bag directories that you would like to add to it.
    """
    if len(args) < 2:
        console.error("You must supply a fondz directory path and a bag path.")
        sys.exit(2)
    fondz.add_bag(*args)



@app(usage="FONDZ_DIR")
def write(args, console):
    """
    Write or re-write HTML files for a given fondz project.
    """
    if len(args) < 1:
        console.error("You must supply a fondz directory path")
        sys.exit(2)
    fondz.write(args[0])
