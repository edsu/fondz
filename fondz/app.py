import sys
import clik
import fondz
import logging

version = '0.0.1'
description = "create automated archival descriptions of digital content"
app = clik.App(
    'fondz',
    version=version,
    description=description
)

@app(usage="FONDZ_DIR BAG1 [BAG2 ...]")
def create(args, console):
    """
    Create a new fondz project.

    Pass in a directory to use for your fondz project, and the path to one or 
    more bag directories.
    """
    if len(args) < 2:
        console.error("You must supply a fondz directory path and at least one bag.")
        sys.exit(2)
    try:
        fondz.create(*args)
    except Exception as e:
        console.error(e)


@app(usage="FONDZ_DIR BAG_DIR")
def add_bag(args, console):
    """
    Create a new fondz project.

    Pass in a directory to use for your fondz project, and the path to one or 
    more bag directories.
    """
    if len(args) < 2:
        console.error("You must supply a fondz directory path and a bag path.")
        sys.exit(2)
    fondz.add_bag(*args)



@app(usage="FONDZ_DIR")
def write(args, console):
    """
    Write or re-write fondz description.
    """
    if len(args) < 1:
        console.error("You must supply a fondz directory path")
        sys.exit(2)
    fondz.write(args[0])
