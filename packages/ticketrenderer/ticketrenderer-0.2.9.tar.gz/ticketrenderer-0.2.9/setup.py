# coding=utf-8

import os
from setuptools import setup

VERSION = "0.2.9"

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ticketrenderer",
    packages = ["ticketrenderer"],
    version = VERSION,
    author = "Benoît Guigal",
    author_email = "benoit@postcardgroup.com",
    description = ("A library used to render Figure tickets from ticket templates"),
    url = "https://github.com/Postcard/ticket-renderer-python",
    download_url = f'https://github.com/Postcard/ticket-renderer-python/tarball/{VERSION}',
    py_modules=('ticketrenderer',),
    install_requires=[
        'jinja2>=2.7.3',
        'mock==1.0.1'
    ]
)
