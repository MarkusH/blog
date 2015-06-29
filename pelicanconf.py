#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

BASE_DIR = os.path.dirname(__file__)

AUTHOR = 'Markus Holtermann'
SITENAME = 'markusholtermann'
SITEURL = 'http://127.0.0.1:8000'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'
LOAD_CONTENT_CACHE = False

PLUGIN_PATHS = (os.path.join(BASE_DIR, 'pelican_plugins'),)
PLUGINS = ['blog.plugins', 'share_post', 'sitemap']

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_FEED_ATOM = 'feeds/tag.%s.atom.xml'
TRANSLATION_FEED_ATOM = None

DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PAGINATION = 15

RELATIVE_URLS = True

DISPLAY_CATEGORIES_ON_MENU = False

PATH = 'content'
PAGE_PATHS = ['pages']
STATIC_PATHS = ['files', 'images']

CATEGORY_EXCLUDES = {'australia'}

THEME = os.path.join(BASE_DIR, 'theme')

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})__((?P<lang>[a-z]{2})__)?(?P<slug>.*)'

TYPOGRIFY = True

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
ARTICLE_LANG_URL = '{lang}/' + ARTICLE_URL
ARTICLE_LANG_SAVE_AS = ARTICLE_LANG_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'
PAGE_LANG_URL = '{lang}/' + PAGE_URL
PAGE_LANG_SAVE_AS = PAGE_LANG_URL + 'index.html'

DOCUTILS_SETTINGS = {
    'math_output': 'MathJAX',
}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,
        'indexes': 0.5,
        'pages': 0.3
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'daily'
    }
}
