import os
import logging
import tempfile

from utils import run, listdir_fullpath

def convert(fondz_dir):
    """
    convert_bags will create a derivatives directory in the supplied
    fondz_dir and try to create web accessible derivatives of all
    the original data. 
    """
    originals_dir = os.path.join(fondz_dir, "originals")
    logging.info("converting %s", originals_dir)
    for bag_name in os.listdir(originals_dir):
        bag_dir = os.path.join(originals_dir, bag_name)
        data_dir = os.path.join(bag_dir, "data")
        target_dir = os.path.join(fondz_dir, "derivatives", bag_name)
        if os.path.isdir(data_dir):
            convert_dir(data_dir, target_dir)


def convert_dir(from_dir, to_dir):
    logging.info("converting %s to %s", from_dir, to_dir)

    for filename in os.listdir(from_dir):
        path = os.path.join(from_dir, filename)

        if not os.path.isdir(to_dir):
            os.mkdir(to_dir)

        if os.path.isdir(path):
            convert_dir(path, os.path.join(to_dir, filename))

        # try to convert the file to html
        tmp_file = convert_to_html(path)
        if not os.path.isfile(tmp_file):
            continue

        # move the temporary html file to the target_dir
        # preserving the path within the src_dir
        new_file = os.path.join(to_dir, filename + ".html")
        logging.info("moving %s to %s", tmp_file, new_file)
        os.rename(tmp_file, new_file)


def convert_to_html(path):
    tmp_dir = tempfile.mkdtemp()
    filename = os.path.basename(path)
    prefix, ext = os.path.splitext(filename)
    html_file = os.path.join(tmp_dir, prefix + ".html")
    cmd = [
        'libreoffice', 
        '--invisible', 
        '--convert-to', 'html:HTML', 
        '--outdir', tmp_dir, 
        path
    ]
    rc, stdout = run(cmd)
    if rc != 0:
        logging.error("convert to html returned non zero: %i", rc)
        return None
    return html_file
