# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.writers.html4css1 import HTMLTranslator

from pelican import signals


class GalleryNode(nodes.bullet_list):
    pass


class Gallery(Directive):
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = True
    option_spec = {
        'small': directives.nonnegative_int,
        'medium': directives.nonnegative_int,
        'large': directives.nonnegative_int,
    }
    has_content = True

    def run(self):
        classes = ['clearing-thumbs']
        if 'small' in self.options:
            classes.append('small-block-grid-%d' % self.options['small'])
        if 'medium' in self.options:
            classes.append('medium-block-grid-%d' % self.options['medium'])
        if 'large' in self.options:
            classes.append('large-block-grid-%d' % self.options['large'])

        cont = GalleryNode(self.content, classes=classes)
        self.state.nested_parse(self.content, self.content_offset, cont)
        figures = cont.children
        cont.clear()
        for fig in figures:
            fig.attributes['classes'].append('th')
            li = nodes.list_item()
            li.append(fig)
            cont.append(li)
        return [cont]


def _visit_GalleryNode(self, node):
    self.body.append(self.starttag(node, 'ul', **{'data-clearing': ''}))


def _depart_GalleryNode(self, node):
    self.body.append('</ul>\n')


def register_rst_directives(readers):
    directives.register_directive('gallery', Gallery)
    setattr(HTMLTranslator, 'visit_GalleryNode', _visit_GalleryNode)
    setattr(HTMLTranslator, 'depart_GalleryNode', _depart_GalleryNode)


def register():
    signals.readers_init.connect(register_rst_directives)
