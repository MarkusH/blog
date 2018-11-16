# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from functools import partial

from docutils.parsers.rst.directives import register_directive
from jinja2.filters import do_striptags as striptags

from pelican import signals
from pelican.contents import Article, Page
from pelican.utils import memoized

from . import directives
from .generators import AMPGenerator
from .imaging import gen_article_thumbnails
from .readers import AMPString, BlogReader


def register():
    """
    Pelican entry point
    """
    register_directives()
    patch_docutils_image()
    patch_article_content_class()
    signals.readers_init.connect(add_reader)
    signals.readers_init.connect(patch_typogrify)
    signals.get_generators.connect(get_generators)
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


def get_generators(pelican_object):
    return AMPGenerator


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


def patch_docutils_image():
    from docutils.parsers.rst.directives import nonnegative_int
    from docutils.parsers.rst.directives.images import Image
    Image.option_spec['scols'] = nonnegative_int
    Image.option_spec['mcols'] = nonnegative_int
    Image.option_spec['lcols'] = nonnegative_int


def patch_article_content_class():
    def __init__(self, content, metadata=None, settings=None, source_path=None, context=None):
        self._amp_content = getattr(content, 'amp_data', None)
        Page.__init__(self, content, metadata=metadata, settings=settings, source_path=source_path, context=context)

    def get_amp_content(self, siteurl):
        if hasattr(self, '_get_amp_content'):
            amp_content = self._get_amp_content()
        else:
            amp_content = self._amp_content
        return self._update_content(amp_content, siteurl)

    def amp_content(self):
        return self.get_amp_content(self.get_siteurl())

    def amp_save_as(self):
        return self.get_url_setting('amp_save_as')

    def amp_url(self):
        return self.get_url_setting('amp_url')

    def json_ld(self):
        image = None
        SITEURL = self.settings['SITEURL']
        if getattr(self, 'image', None):
            image = {
                '@type': 'ImageObject',
                'url': '%s/images/thumb/%s-1012x422.jpg' % (
                    SITEURL, self.image.rpartition('.')[0]
                ),
                'width': 1012,
                'height': 422,
            }
        data = {
            '@context': 'http://schema.org',
            '@type': 'BlogPosting',
            'headline': striptags(self.title),
            'image': image,
            'keywords': ', '.join(sorted(map(str, self.tags))),
            'url': '%s/%s' % (SITEURL, self.url),
            'datePublished': self.date.isoformat(),
            'dateModified': getattr(self, 'modified', self.date).isoformat(),
            'description': striptags(self.summary),
            'publisher': {
                '@type': 'Person',
                'name': 'Markus Holtermann',
            },
            'mainEntityOfPage': '%s/%s' % (SITEURL, self.url),
            'author': [{
                '@type': 'Person',
                'name': str(author),
                'url': '%s/%s' % (SITEURL, author.url),
            } for author in self.authors],
        }
        data = {
            k: v
            for k, v in data.items()
            if v is not None
        }
        return json.dumps(data)

    Article.__init__ = __init__
    Article.get_amp_content = memoized(get_amp_content)
    Article.amp_content = property(amp_content)
    Article.amp_save_as = property(amp_save_as)
    Article.amp_url = property(amp_url)
    Article.json_ld = property(json_ld)


def patch_typogrify(readers):
    try:
        from typogrify import filters
    except ImportError:
        return

    def typogrify_wrapper(text, ignore_tags=None):
        from typogrify.filters import _typogrify
        ignore_tags = ignore_tags or []
        ignore_tags.append('math')
        content = _typogrify(text, ignore_tags=ignore_tags)
        if isinstance(text, AMPString):
            amp_data = text.amp_data
            content = AMPString(content)
            content.amp_data = _typogrify(amp_data, ignore_tags=ignore_tags)
        return content

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
            content = smartypants.smartypants(text, attr=attr)
            if isinstance(text, AMPString):
                amp_data = text.amp_data
                content = AMPString(content)
                content.amp_data = smartypants.smartypants(amp_data, attr=attr)
            return content

    setattr(filters, 'smartypants', smartypants_wrapper)

    setattr(filters, 'widont', lambda text: text)
