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
            span = []
            try:
                span.extend(fig.children[0].attributes['classes'])
            except IndexError:
                try:
                    span.extend(fig.attributes['classes'])
                except IndexError:
                    pass
            li.attributes['classes'].extend(span)
            li.append(fig)
            cont.append(li)
        return [cont]


methods = []
moves = [
    ('visit_math', '_visit_math'),
]


def register_method(f):
    methods.append((f.__name__, f))
    return f


@register_method
def visit_GalleryNode(self, node):
    self.body.append(self.starttag(node, 'ul', **{'data-clearing': ''}))


@register_method
def depart_GalleryNode(self, node):
    self.body.append('</ul>\n')


@register_method
def visit_math(self, node, math_env=''):
    try:
        self._visit_math(node, math_env)
    except nodes.SkipNode:
        # content processed
        if '</div>' in self.body[-1] and '<div class="math">' in self.body[-4]:
            self.body[-1] = '</math>\n'
            self.body[-4] = '<math>\n'
    raise nodes.SkipNode


@register_method
def visit_section(self, node):
    self.section_level += 1


@register_method
def depart_section(self, node):
    self.section_level -= 1


def register_rst_directives(readers):
    directives.register_directive('gallery', Gallery)

    for old, new in moves:
        if not hasattr(HTMLTranslator, new):
            old_method = getattr(HTMLTranslator, old)
            setattr(HTMLTranslator, new, old_method)

    for name, method in methods:
        setattr(HTMLTranslator, name, method)


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
            raise TypogrifyError("Error in {% smartypants %} filter: The Python smartypants library isn't installed.")
        else:
            attr = smartypants.default_smartypants_attr | smartypants.Attr.w
            output = smartypants.smartypants(text, attr=attr)
            return output

    setattr(filters, 'smartypants', smartypants_wrapper)

    setattr(filters, 'widont', lambda text: text)


def register():
    signals.readers_init.connect(register_rst_directives)
    signals.readers_init.connect(patch_typogrify)
