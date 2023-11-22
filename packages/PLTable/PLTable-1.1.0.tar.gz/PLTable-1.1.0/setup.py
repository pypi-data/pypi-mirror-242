#!/usr/bin/env python3
# coding=utf-8

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='PLTable',
    version='1.1.0',
    license='BSD (3 clause)',
    description='Python 3 library for easily displaying tabular data in a visually appealing text table format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luke Maurits, Kane Blueriver, Ryan James, Plato Mavropoulos',
    maintainer='Plato Mavropoulos',
    url='https://github.com/platomav/PLTable',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing'
    ],
)
