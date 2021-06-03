#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.


sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = "https://markusholtermann.eu"
RELATIVE_URLS = False
LOAD_CONTENT_CACHE = True

DELETE_OUTPUT_DIRECTORY = True
