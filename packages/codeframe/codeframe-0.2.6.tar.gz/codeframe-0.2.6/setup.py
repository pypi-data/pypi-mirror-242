#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="codeframe",
    description="Creates a simple package structure, git, PyPI, bumpversion, pytest and configfile ready",
    author="jaromrax",
    author_email="jaromrax@gmail.com",
    url = "http://gitlab.com/jaromrax/codeframe",
    license="GPL2",
    version=get_version("codeframe/version.py"),
    packages=['codeframe'],
    package_data={'codeframe': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/codeframe'],
    install_requires = ['fire'],
)
