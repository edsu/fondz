import os

from fondz.utils import render_to

def create(fondz_dir, *bags, **kwargs):
    if not os.path.isdir(fondz_dir):
        os.mkdir(fondz_dir)

    index_file = os.path.join(fondz_dir, "index.html")
    html = render_to('index.html', index_file)
