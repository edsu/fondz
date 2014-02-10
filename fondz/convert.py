import os
import logging
import tempfile

from os.path import abspath, join, isdir, isfile, basename, splitext

from utils import run, listdir_fullpath

logger = logging.getLogger("fondz")


def convert(from_dir, to_dir):
    logger.debug("converting %s to %s", from_dir, to_dir)
    from_dir = abspath(from_dir)
    to_dir = abspath(to_dir)

    for filename in os.listdir(from_dir):
        path = join(from_dir, filename)

        if not isdir(to_dir):
            os.mkdir(to_dir)

        if isdir(path):
            convert(path, join(to_dir, filename))

        # try to convert the file to html
        tmp_file = convert_to_html(path)
        if not isfile(tmp_file):
            continue

        # move the temporary html file to the target_dir
        # preserving the path within the src_dir
        new_file = join(to_dir, filename + ".html")
        logger.debug("moving %s to %s", tmp_file, new_file)
        os.rename(tmp_file, new_file)


def convert_to_html(path):
    tmp_dir = tempfile.mkdtemp()
    filename = basename(path)
    prefix, ext = splitext(filename)
    html_file = join(tmp_dir, prefix + ".html")
    cmd = [
        'libreoffice', 
        '--invisible', 
        '--convert-to', 'html:HTML', 
        '--outdir', tmp_dir, 
        path
    ]
    rc, stdout = run(cmd)
    if rc != 0:
        logger.error("convert to html returned non zero: %i", rc)
        return None
    return html_file
