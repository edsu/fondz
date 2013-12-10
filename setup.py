#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

from invenstory.utils import which


if not which('mallet'):
    print "you must install Mallet and make it available in your PATH"
    sys.exit(1)

if not which('libreoffice'):
    print "you must install LibreOffice and make it available in your PATH"
    sys.exit(1)


setup(
        name = 'invenstory',
        version = '0.0.1',
        url = 'http://github.com/edsu/invenstory',
        author = 'Ed Summers',
        author_email = 'ehs@pobox.com',
        packages = ['invenstory'],
        scripts = ['scripts/invenstory'],
        test_suite = 'tests',)
