#!/usr/bin/env python

import os

from setuptools import setup, find_packages

# make sure mallet is available

has_mallet = False
for path in os.environ["PATH"].split(os.pathsep):
    path = path.strip('"')
    mallet = os.path.join(path, 'mallet')
    if os.path.isfile(mallet) and os.access(mallet, os.X_OK):
        has_mallet = True
if not has_mallet:
    print "you must install Mallet and make it available in your path"
    sys.exit(1)

setup(
        name = 'diagnidnif',
        version = '0.0.1',
        url = 'http://github.com/edsu/diagnidnif',
        author = 'Ed Summers',
        author_email = 'ehs@pobox.com',
        packages = ['diagnidnif'],
        scripts = ['scripts/diagnidnif'],
        test_suite = 'tests',)
