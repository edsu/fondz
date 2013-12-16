import os
import tempfile

from utils import run

def convert(src_dir, target_dir):
    return True

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
        raise Exception("unable to convert %s" % path)
    return html_file
