#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='homepage',
    version='0.0.0',
    description='Homepage scripts',
    long_description='Homepage scripts',
    author='Markus Holtermann',
    author_email='info@markusholtermann.eu',
    url='https://github.com/Markush2010/blog',
    # packages=[],
    # package_dir={'importer': 'importer'},
    # include_package_data=True,
    license="BSD",
    entry_points='''
        [pygments.lexers]
        jni = pygments_lexer:JNILexer
    ''',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
)
