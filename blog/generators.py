# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from functools import partial
from itertools import chain

from pelican import signals
from pelican.generators import ArticlesGenerator


class AMPGenerator(ArticlesGenerator):
    """Generate blog articles"""

    def __init__(self, *args, **kwargs):
        """initialize properties"""
        self.articles = []  # only articles in default language
        self.translations = []
        super(AMPGenerator, self).__init__(*args, **kwargs)
        signals.article_generator_init.send(self)

    def get_template(self, name):
        """
        Return the AMP template name
        """
        return super(AMPGenerator, self).get_template('%s.amp' % name)

    def generate_articles(self, write):
        """Generate the articles."""
        for article in chain(self.translations, self.articles):
            if not article.save_as.endswith('.html'):
                logging.error('[SKIP] Not an .html article file: %r %s' % (article, article.save_as))
                continue
            write(
                article.amp_save_as,
                self.get_template(article.template),
                self.context,
                article=article,
                category=article.category,
                override_output=hasattr(article, 'override_save_as'),
                blog=True,
            )

    def generate_output(self, writer):
        write = partial(writer.write_file, relative_urls=self.settings['RELATIVE_URLS'])
        self.generate_articles(write)
        signals.article_writer_finalized.send(self, writer=writer)
