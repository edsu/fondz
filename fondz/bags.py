import os
import re

from fondz.utils import listdir_fullpath, write_json

def bags(fondz_dir):
    """ 
    generates a JSON summary of what's in the bags
    """
    fondz_dir = os.path.abspath(fondz_dir)
    results = {
        'bags': [],
        'num_files': 0,
        'bytes': 0
    }
    originals_dir = os.path.join(fondz_dir, "originals")

    for bag in os.listdir(originals_dir):
        # TODO: look for other manifest types?
        bag_dir = os.path.join(originals_dir, bag)
        manifest = os.path.join(bag_dir, "manifest-md5.txt")
        b = {
            "files": [],
            "bytes": 0,
        }
        for line in open(manifest):
            line = line.strip()
            cols = re.split(r' +', line)
            path = os.path.join(bag_dir, cols[1])
            st = os.stat(path)
            rel_path = os.path.join("originals", bag, path)
            b['bytes'] += st.st_size
            b['files'].append({
                "path": rel_path,
                "bytes": st.st_size,
                "created": st.st_ctime,
                "modified": st.st_mtime,
                "md5": cols[0]
            })
        results['bytes'] += b['bytes']
        results['num_files'] += len(b['files'])
        results['bags'].append(b)

    bags_json = os.path.join(fondz_dir, "js", "bags.json")
    write_json(results, bags_json)
    return results

