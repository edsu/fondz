import os
import json
import jinja2
import logging
import subprocess


def which(program):
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe = os.path.join(path, program)
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            return exe
    return None


def run(cmd):
    logging.info("starting command %s", cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stderr:
        line = line.strip()
        logging.error(line)
    p.wait()
    logging.info("finished command, exit code %s", p.returncode)
    return p.returncode, p.stdout


def write_json(d, filename):
    open(filename, "w").write(json.dumps(d, indent=2))


tmpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja = jinja2.Environment(loader=jinja2.PackageLoader('fondz', 'templates'))


def render(template, *args, **kwargs):
    t = jinja.get_template(template)
    return t.render(*args, **kwargs)


def render_to(template, html_file, *args, **kwargs):
    html = render(template, *args, **kwargs)
    open(html_file, "w").write(html)
