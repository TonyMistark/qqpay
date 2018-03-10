#!/usr/bin/env python
from __future__ import with_statement, print_function

try:
    # python setup.py test
    import multiprocessing  # NOQA
except ImportError:
    pass

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    pass


cmdclass = {}
# cmdclass['test'] = PyTest

# readme = 'README.md'
# with open(readme, 'rb') as f:
#     long_description = f.read().decode('utf-8')
# import os
# print("pwd-->", os.getcwd())
# with open('requirements.txt') as f:
#     requirements = [l for l in f.read().splitlines() if l]

# NAME = "qqpay"
# PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]

setup(
    name='qqpay-python-sdk',
    version='0.0.1',
    author='ice',
    author_email='ice@kaiheikeji.com',
    url='git@github.com:TonyMistark/qqpay.git',
    packages=find_packages(),
    keywords='qqpay, qpay, Qpay',
    description='Qqpay: Qqpay SDK for Python',
    long_description="Qqpay: Qqpay SDK for Python",
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
