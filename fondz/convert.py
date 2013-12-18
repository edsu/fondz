import os
import logging
import tempfile

from utils import run

def convert_dir(src_dir, target_dir):

    for filename in os.listdir(src_dir):
        path = os.path.join(src_dir, filename)

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        if os.path.isdir(path):
            convert_dir(path, os.path.join(target_dir, filename))

        # try to convert the file to html
        tmp_file = convert_to_html(path)
        if not os.path.isfile(tmp_file):
            continue

        # move the temporary html file to the target_dir
        # preserving the path within the src_dir
        new_file = os.path.join(target_dir, filename + ".html")
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
    rc = run(cmd)
    if rc != 0:
        logging.error("convert to html returned non zero: %i", rc)
        return None
    return html_file
