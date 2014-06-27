#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTHOR = 'Markus Holtermann'
SITENAME = 'markusholtermann.eu'
SITEURL = 'http://127.0.0.1:8000'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

PLUGIN_PATHS = (os.path.join(BASE_DIR, 'pelican-plugins'),)
PLUGINS = ['plugins']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
    ('Arch Linux', 'http://archlinux.org/'),
    ('aufgebauscht', 'http://blog.fbausch.de/'),
    ('Gentoo', 'http://www.gentoo.org/'),
    ('Ubuntu', 'http://ubuntu.com/'),
    ('ubuntuusers.de', 'http://ubuntuusers.de/'),
)

# Social widget
SOCIAL = (
    ('Google+', 'https://plus.google.com/+MarkusHoltermann'),
    ('Twitter', 'https://twitter.com/m_holtermann'),
)

DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PAGINATION = 5

RELATIVE_URLS = True

DISPLAY_CATEGORIES_ON_MENU = False

PAGE_PATHS = ('pages',)
STATIC_PATHS = ('images',)

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
