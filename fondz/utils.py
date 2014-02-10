import os
import json
import jinja2
import logging
import subprocess

from os.path import isfile, join, dirname

logger = logging.getLogger("fondz")


def which(program):
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe = join(path, program)
        if isfile(exe) and os.access(exe, os.X_OK):
            return exe
    return None


def run(cmd):
    logger.debug("starting command %s", cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stderr:
        line = line.strip()
        logger.debug(line)
    p.wait()
    logger.debug("finished command, exit code %s", p.returncode)
    return p.returncode, p.stdout


def write_json(d, filename):
    logger.debug("writing %s", filename)
    open(filename, "w").write(json.dumps(d, indent=2))


def read_json(filename):
    logger.debug("reading %s", filename)
    return json.loads(open(filename).read())


def render(template, *args, **kwargs):
    t = jinja.get_template(template)
    return t.render(*args, **kwargs)


def render_to(template, html_file, *args, **kwargs):
    html = render(template, *args, **kwargs)
    open(html_file, "w").write(html)


def listdir_fullpath(d):
    return [join(d, f) for f in os.listdir(d)]


def template_dir():
    return join(dirname(__file__), 'templates')


jinja = jinja2.Environment(loader=jinja2.PackageLoader('fondz', 'templates'))
