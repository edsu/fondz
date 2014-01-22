#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

from fondz.utils import which


if not which('mallet'):
    print "you must install Mallet and make it available in your PATH"
    sys.exit(1)

if not which('libreoffice'):
    print "you must install LibreOffice and make it available in your PATH"
    sys.exit(1)

if not which('exiftool'):
    print "you must install exiftool and make it available in your PATH"
    sys.exit(1)


setup(
        name = 'fondz',
        version = '0.0.1',
        url = 'http://github.com/edsu/fondz',
        author = 'Ed Summers',
        author_email = 'ehs@pobox.com',
        packages = find_packages(),
        scripts = ['scripts/fondz'],
        package_data = {'fondz': [
        		'templates/*.html',
        		'templates/css/*',
        		'templates/img/*',
        		'templates/js/*.js',
        		'templates/js/vendor/*',
        		'templates/js/foundation/*'
        	]},
        test_suite = 'tests',)
