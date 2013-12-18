import os

def create(fondz_dir, *bags, **kwargs):
    if not os.path.isdir(fondz_dir):
        os.mkdir(fondz_dir)
    index = open(os.path.join(fondz_dir, "index.html"), 'w')
    index.close()
    return True


