from docutils import nodes
from pelican.readers import PelicanHTMLTranslator

__all__ = ['BlogHTMLTranslator']


class GalleryTranslator:

    def visit_gallery_node(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='row gallery'))
        for image in node.images:
            self.body.append(self.starttag(image, 'a', HREF='/images/' + image.source))
            self.body.append(self.starttag(node, 'picture', CLASS='activator'))
            self.body.append('<!--[if IE 9]><video style="display: none;"><![endif]-->')
            self.body.append('<source srcset="/images/thumb/%s" media="(min-width: 993px)">' % image.thumbs[2])
            self.body.append('<source srcset="/images/thumb/%s" media="(min-width: 601px)">' % image.thumbs[1])
            self.body.append('<!--[if IE 9]></video><![endif]-->')
            self.body.append('<img srcset="/images/thumb/%s" alt="%s">' % (image.thumbs[0], image['alt']))
            self.body.append('</picture>')
            self.body.append('</a>')

    def depart_gallery_node(self, node):
        self.body.append('</div>')


class ProjectTranslator:
    pass

    def visit_project_node(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='project'))
        self.body.append(self.starttag(node, 'div', CLASS='row'))
        self.body.append(self.starttag(node, 'ul', **{
            'class': 'collapsible',
            'data-collapsible': 'expandable',
        }))

    def depart_project_node(self, node):
        self.body.append('</ul>')
        self.body.append('</div>')
        self.body.append('</div>')

    def visit_project_desc(self, node):
        self.body.append(self.starttag(node, 'li'))
        self.body.append(self.starttag(node, 'div', CLASS='collapsible-header active'))
        self.body.append(self.starttag(node, 'h3'))
        self.body.append(node.name)
        self.body.append('</h3>')
        self.body.append('</div>')
        self.body.append(self.starttag(node, 'div', CLASS='collapsible-body'))
        self.body.append(self.starttag(node, 'p'))

    def depart_project_desc(self, node):
        self.body.append('</p>')
        self.body.append('</div>')
        self.body.append('</li>')

    def _visit_project_item(self, node):
        self.body.append(self.starttag(node, 'li'))
        self.body.append(self.starttag(node, 'div', CLASS='collapsible-header active'))
        self.body.append(self.starttag(node, 'i', CLASS=node.icon))
        self.body.append('</i>')
        self.body.append(node.label)
        self.body.append(': ')
        self.body.append(self.starttag(node, 'span', CLASS='hide-on-med-and-down'))

    visit_project_code = _visit_project_item
    visit_project_docs = _visit_project_item
    visit_project_download = _visit_project_item
    visit_project_homepage = _visit_project_item
    visit_project_license = _visit_project_item

    def _depart_project_item(self, node):
        start = (len(self.body) - 1) - self.body[::-1].index('<span class="hide-on-med-and-down">\n')
        content = self.body[start + 1:]
        self.body.append('</span>')
        self.body.append('</div>')
        self.body.append(self.starttag(node, 'div', CLASS='collapsible-body hide-on-large-only'))
        self.body.append(self.starttag(node, 'p'))
        self.body.extend(content)
        self.body.append('</p>')
        self.body.append('</div>')
        self.body.append('</li>')

    depart_project_code = _depart_project_item
    depart_project_docs = _depart_project_item
    depart_project_download = _depart_project_item
    depart_project_homepage = _depart_project_item
    depart_project_license = _depart_project_item


class BlogHTMLTranslator(GalleryTranslator, ProjectTranslator,
                         PelicanHTMLTranslator):

    def visit_math(self, node, math_env=''):
        try:
            PelicanHTMLTranslator.visit_math(self, node, math_env=math_env)
        except nodes.SkipNode:
            # content processed
            if '</div>' in self.body[-1] and '<div class="math">' in self.body[-4]:
                self.body[-1] = '</math>\n'
                self.body[-4] = '<math>\n'
        raise nodes.SkipNode

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1
