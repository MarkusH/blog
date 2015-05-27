from __future__ import unicode_literals

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.transforms import parts

from .nodes import (
    gallery_node, project_code, project_desc, project_docs, project_download,
    project_homepage, project_license, project_node,
)


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

        cont = gallery_node(self.content, classes=classes)
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
