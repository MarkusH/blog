#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="homepage",
    version="0.0.0",
    description="The code and content on markusholtermann.eu",
    author="Markus Holtermann",
    author_email="info@markusholtermann.eu",
    url="https://github.com/MarkusH/blog",
    packages=find_packages(),
    license="BSD",
    entry_points="""
        [pygments.lexers]
        jni = blog.pygments_lexer:JNILexer
    """,
    zip_safe=False,
)
