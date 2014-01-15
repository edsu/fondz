import os
import csv
import logging

from utils import run, which, write_json

fido = which("fido.py")


def identify(fondz_dir):
    """
    Will run identification over the source bags, and write out the
    format report to the js/formats.json file in the fondz directory.
    """
    results = []
    src_dir = os.path.join(fondz_dir, "originals")
    for f in os.listdir(src_dir):
        data_dir = os.path.join(src_dir, f, 'data')
        if os.path.isdir(data_dir):
            results.extend(identify_dir(data_dir))

    for f in results:
        f['path'] = os.path.relpath(f['path'], fondz_dir)

    formats_file = os.path.join(fondz_dir, "js", "formats.json")
    write_json(results, formats_file)

    return results


def identify_dir(d):
    logging.info("starting format identification for %s", d)
    d = os.path.abspath(d)

    formats = []
    rc, output = run([fido, "-r", d])
    reader = csv.reader(output)
    for row in reader:
        m = {
            "path": row[6],
            "name": row[3],
            "description": row[4],
            "mediatype": row[7],
        }
        logging.info("got %s", m)
        formats.append(m)

    return formats


def summarize(formats):
    counts = {}
    for f in formats:
        name = f['name']
        if name not in counts:
            counts[name] = []
        counts[name].append(f['path'])
    sorted_names = counts.keys()
    sorted_names.sort(lambda a, b: cmp(len(counts[b]), len(counts[a])))
    return [{'name': m, 'files': counts[m]} for m in sorted_names]

