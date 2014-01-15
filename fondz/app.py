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

logging = logging.basicConfig(
    filename='fondz.log', 
    format='%(asctime)-15s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@app(usage="FONDZ_DIR BAG1 [BAG2 ...]")
def create(args, console):
    """
    Create a new fondz project.

    Pass in a directory to use for your fondz project, and the path to one or 
    more bag directories.
    """
    if len(args) < 2:
        console.error("You must supply a fondz directory path and a at least one bag.")
        sys.exit(2)
    fondz.create(*args)


@app(usage="FONDZ_DIR")
def topics(args, console):
    """
    Generate (or re-generate) topic modeling for a fondz directory.
    """
    if len(args) < 1:
        console.error("You must supply a fondz directory path")
        sys.exit(2)
    fondz.topics(args[0])


@app(usage="FONDZ_DIR")
def identify(args, console):
    """
    Run (or re-run) format identification for a fondz directory.
    """
    if len(args) < 1:
        console.error("You must supply a fondz directory path")
        sys.exit(2)
    fondz.identify(args[0])

@app(usage="FONDZ_DIR")
def write(args, console):
    """
    Write or re-write fondz description.
    """
    if len(args) < 1:
        console.error("You must supply a fondz directory path")
        sys.exit(2)
    fondz.write(args[0])

