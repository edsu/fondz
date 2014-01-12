import os
import csv
import magic
import logging

from utils import run, which

fido = which("fido.py")


def identify(fondz_dir):
    results = []
    src_dir = os.path.join(fondz_dir, "originals")
    for f in os.listdir(src_dir):
        data_dir = os.path.join(src_dir, f, 'data')
        if os.path.isdir(data_dir):
            results.extend(identify_dir(data_dir))

    for f in results:
        f['path'] = os.path.relpath(f['path'], fondz_dir)

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

