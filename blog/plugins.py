# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


def register_directives():
    register_directive('gallery', directives.Gallery)
    register_directive('project', directives.Project)
    register_directive('pngmath', directives.PNGMath)


def add_reader(readers):
    readers.reader_classes['rst'] = BlogReader


def thumbnail_generator(article_generator):
    for article in article_generator.articles:
        if hasattr(article, 'image'):
            gen_article_thumbnails(article.image)


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
