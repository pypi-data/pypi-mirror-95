#!/usr/bin/env python

# Warning: Please do not upload setup.py to github: https://github.com/bhexopen/BHEX-OpenApi/tree/master/sdk/python

import codecs
import os

from broker import version

from setuptools import setup, find_packages

description = "Python SDK for Broker REST And Websocket API"

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


setup(
    name="broker-trade-client",
    version=version,
    author="tufei",
    author_email="tufei8438@gmail.com",
    description=description,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/bhexopen/BHEX-OpenApi/tree/master/sdk/python",
    packages=find_packages(),
    install_requires=['requests', 'six', 'twisted', 'autobahn', 'pyopenssl', 'service_identity'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)