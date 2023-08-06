#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dataclass_factory',
    description='An utility class for creating instances of dataclasses',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='2.10.1',
    url='https://github.com/tishka17/dataclass_factory',
    author='A. Tikhonov',
    author_email='17@itishka.org',
    license='Apache2',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    packages=['dataclass_factory'],
    install_requires=[
        'dataclasses;python_version<"3.7"',
    ],
    package_data={
        'dataclass_factory': ['py.typed'],
    },
    python_requires=">=3.6",
)
