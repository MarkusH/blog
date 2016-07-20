from __future__ import unicode_literals

import math

from docutils import nodes
from docutils.parsers.rst import directives, Directive

from .imaging import gen_article_thumbnails, gen_equation_image
from .nodes import (
    gallery_node, pngmath, project_code, project_desc, project_docs,
    project_download, project_homepage, project_license, project_node,
    speakerdeck,
)


NUM_COLS = 6
GUTTER_WIDTH = 10.5


class Gallery(Directive):
    required_arguments = 0
    optional_arguments = 4
    final_argument_whitespace = True
    option_spec = {
        'small': directives.nonnegative_int,
        'medium': directives.nonnegative_int,
        'large': directives.nonnegative_int,
        'nocrop': directives.flag,
    }
    has_content = True

    def run(self):
        gallery = gallery_node(self.content)
        self.state.nested_parse(self.content, self.content_offset, gallery)
        images = gallery.children
        gallery.clear()
        gallery.images = []

        max_widths = {
            's': 500.594,
            'm': 768.688,
            'l': 1007.906,
        }
        # Determine the number of images per row for every resolution, fall
        # back to the count for the next lower resolution if non specified.
        counts = {}
        counts['s'] = self.options.get('small', 1)
        counts['m'] = self.options.get('medium', counts['s'])
        counts['l'] = self.options.get('large', counts['m'])
        # When flag is set: True, else False
        crop = self.options.get('nocrop', True) is not None

        # We use a 6-column grid. How many columns does each image span per
        # size normally, not accounting for extra wide images.
        spans = {k: NUM_COLS / v for k, v in counts.items()}

        for img in images:
            classes = ['col']
            sizes = []
            last_col_span = 1
            for key in ('s', 'm', 'l'):
                # Check if we should use a multiple of the default columns
                multiplier = img.attributes.get('%scols' % key, last_col_span)
                last_col_span = multiplier
                # Create the CSS classes, e.g. s6, m3, l3
                classes.append('%s%d' % (key, spans[key] * multiplier))
                # Total padding on left and right and between all images in this row
                # - 10.5 is the padding in px
                # - * 2 is for either side of the image
                # - counts[key] is the number of images in a row
                # - multiplier is 1 except for wide images
                padding_w = GUTTER_WIDTH * (counts[key] - multiplier + 1) * 2
                width = int(math.ceil((max_widths[key] - padding_w) * multiplier / counts[key]))
                padding_h = GUTTER_WIDTH * counts[key] * 2
                height = int(math.ceil((max_widths[key] - padding_h) / counts[key]))
                sizes.append((width, height))
            img['classes'].extend(classes)
            target = img.attributes.get('uri', img.attributes.get('refuri'))
            assert target
            img.source = target
            img.thumbs = gen_article_thumbnails(target, sizes=sizes, crop=crop)
            gallery.images.append(img)
        return [gallery]


class Project(Directive):
    required_arguments = 1
    option_spec = {
        'code': directives.unchanged,
        'docs': directives.unchanged,
        'download': directives.unchanged,
        'homepage': directives.unchanged,
        'license': directives.unchanged,
    }
    has_content = True

    def run(self):
        self.assert_has_content()
        document = self.state_machine.document
        text = '\n'.join(self.content)
        project = project_node(text)

        name = nodes.fully_normalize_name(self.arguments[0])
        if not document.has_name(name):
            project['names'].append(name)
        document.note_implicit_target(project)

        desc = project_desc(self.arguments[0])
        self.state.nested_parse(self.content, self.content_offset, desc)
        project += desc

        for key, cls in (
            ('code', project_code),
            ('docs', project_docs),
            ('download', project_download),
            ('homepage', project_homepage),
            ('license', project_license),
        ):
            if key in self.options:
                item = cls()
                textnodes, messages = self.state.inline_text(
                    self.options[key], self.content_offset
                )
                item += textnodes
                item += messages
                project += item

        return [project]


class PNGMath(Directive):
    option_spec = {
        'width': directives.unchanged,
    }
    has_content = True

    def run(self):
        self. assert_has_content()
        filename = gen_equation_image(self.content)
        node = pngmath(src=filename)
        if 'width' in self.options:
            node.width = self.options.get('width', None)
        return [node]


class Speakerdeck(Directive):
    required_arguments = 1
    option_spec = {
        'ratio': directives.unchanged,
    }
    has_content = False

    def run(self):
        node = speakerdeck(
            key=self.arguments[0],
            ratio=self.options.get('ratio', '1.3333333333')
        )
        return [node]
