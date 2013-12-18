import os
import magic

mediatype = magic.Magic(mime=True)
description = magic.Magic()

def identify_dir(src_dir):
    formats = []
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(path, src_dir)
            f_mediatype = mediatype.from_file(path)
            f_desc = description.from_file(path)
            formats.append({
                "path": rel_path, 
                "mediatype": f_mediatype,
                "description": f_desc
            })
    return formats
