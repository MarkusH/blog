# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from docutils.parsers.rst.directives import register_directive

from pelican import signals

from . import directives
from .imaging import gen_article_thumbnails
from .readers import BlogReader


def register():
    """
    Pelican entry point
    """
    register_directives()
    signals.readers_init.connect(add_reader)
    signals.readers_init.connect(patch_typogrify)
    signals.article_generator_finalized.connect(thumbnail_generator)
    signals.article_generator_finalized.connect(exclude_articles_from_index)
    signals.article_writer_finalized.connect(write_excluded_articles)


def register_directives():
    register_directive('gallery', directives.Gallery)
    register_directive('project', directives.Project)
    register_directive('pngmath', directives.PNGMath)
    register_directive('speakerdeck', directives.Speakerdeck)


def add_reader(readers):
    readers.reader_classes['rst'] = BlogReader


def thumbnail_generator(article_generator):
    for article in article_generator.articles:
        if hasattr(article, 'image'):
            gen_article_thumbnails(article.image)


def exclude_articles_from_index(article_generator):
    excludes = article_generator.settings.get('CATEGORY_EXCLUDES')
    articles = [x for x in article_generator.articles if x.category not in excludes]
    delayed = [x for x in article_generator.articles if x.category in excludes]
    article_generator.articles = articles
    article_generator.articles_delayed = delayed


def write_excluded_articles(article_generator, writer):
    article_generator.articles, article_generator.articles_delayed = (
        article_generator.articles_delayed, article_generator.articles
    )
    translations = article_generator.translations
    article_generator.translations = []
    write = partial(writer.write_file, relative_urls=article_generator.settings['RELATIVE_URLS'])
    article_generator.generate_articles(write)
    article_generator.articles, article_generator.articles_delayed = (
        article_generator.articles_delayed, article_generator.articles
    )
    article_generator.translations = translations


def patch_typogrify(readers):
    try:
        from typogrify import filters
    except ImportError:
        return

    def typogrify_wrapper(text, ignore_tags=None):
        from typogrify.filters import _typogrify
        ignore_tags = ignore_tags or []
        ignore_tags.append('math')
        return _typogrify(text, ignore_tags=ignore_tags)

    if not hasattr(filters, '_typogrify'):
        setattr(filters, '_typogrify', getattr(filters, 'typogrify'))
        setattr(filters, 'typogrify', typogrify_wrapper)

    def smartypants_wrapper(text):
        try:
            import smartypants
        except ImportError:
            from typogrify.filters import TypogrifyError
            raise TypogrifyError(
                "Error in {% smartypants %} filter: The Python smartypants "
                "library isn't installed."
            )
        else:
            attr = smartypants.default_smartypants_attr | smartypants.Attr.w
            output = smartypants.smartypants(text, attr=attr)
            return output

    setattr(filters, 'smartypants', smartypants_wrapper)

    setattr(filters, 'widont', lambda text: text)
