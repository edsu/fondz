#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

from inventstory.utils import which


if not which('mallet'):
    print "you must install Mallet and make it available in your PATH"
    sys.exit(1)

if not which('libreoffice'):
    print "you must install LibreOffice and make it available in your PATH"
    sys.exit(1)


setup(
        name = 'inventstory',
        version = '0.0.1',
        url = 'http://github.com/edsu/inventstory',
        author = 'Ed Summers',
        author_email = 'ehs@pobox.com',
        packages = ['inventstory'],
        scripts = ['scripts/inventstory'],
        test_suite = 'tests',)
