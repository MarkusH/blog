import re
from os.path import join

import PIL
from docutils import nodes
from pelican.readers import PelicanHTMLTranslator

__all__ = ['BlogHTMLTranslator']


class GalleryTranslator:

    def visit_gallery_node(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='row gallery'))
        for image in node.images:
            self.body.append(self.starttag(image, 'a', HREF='/images/' + image.source))
            self.body.append(
                '<img class="large lazyload" data-src="/images/thumb/%s" alt="%s" title="%s">'
                % (image.thumbs[2], image['alt'], image['alt'])
            )
            self.body.append(
                '<img class="medium lazyload" data-src="/images/thumb/%s" alt="%s" title="%s">'
                % (image.thumbs[1], image['alt'], image['alt'])
            )
            self.body.append(
                '<img class="small lazyload" data-src="/images/thumb/%s" alt="%s" title="%s">'
                % (image.thumbs[0], image['alt'], image['alt'])
            )
            self.body.append('</a>')

    def depart_gallery_node(self, node):
        self.body.append('</div>')


class ProjectTranslator:

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


class PNGMathTranslator:

    def visit_pngmath(self, node):
        self.body.append('<div class="math center">')
        self.body.append(node.emptytag())

    def depart_pngmath(self, node):
        self.body.append('</div>')


class SpeakerdeckTranslator:

    def visit_speakerdeck(self, node):
        key = node['key']
        ratio = node['ratio']
        self.body.append('<div class="speakerdeck">')
        self.body.append(
            '<script async class="speakerdeck-embed" data-id="{key}" '
            'data-ratio="{ratio}" '
            'src="//speakerdeck.com/assets/embed.js">'.format(
                key=key, ratio=ratio,
            )
        )

    def depart_speakerdeck(self, node):
        self.body.append('</script></div>')


class BlogHTMLTranslator(GalleryTranslator, ProjectTranslator,
                         PNGMathTranslator, SpeakerdeckTranslator,
                         PelicanHTMLTranslator):

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1


class AMPTranslator(BlogHTMLTranslator):

    def visit_gallery_node(self, node):
        self.body.append(self.starttag(node, 'amp-carousel', WIDTH=1, HEIGHT=1, LAYOUT='responsive', TYPE='slides'))
        for image in node.images:
            self.body.append('<div class="slide">')
            src = join('content', 'images', 'thumb', image.thumbs[2])
            width, height = PIL.Image.open(src).size
            image.attributes['classes'] = []
            self.body.append(self.starttag(
                image, 'amp-img',
                SRC='/images/thumb/%s' % image.thumbs[2],
                WIDTH=width, HEIGHT=height, LAYOUT='responsive', alt=image['alt'], title=image['alt']
            ).strip())
            self.body.append('</amp-img>')
            self.body.append('<div class="caption">')
            self.body.append(image['alt'])
            self.body.append('</div>')
            self.body.append('</div>\n')

    def depart_gallery_node(self, node):
        self.body.append('</amp-carousel>')

    RE_IMAGE_CLASSES = re.compile(r'class="([^"]+)"')

    def visit_image(self, node):
        super().visit_image(node)
        last = self.body[-1]
        if last.startswith('<img '):
            kwargs = {
                'LAYOUT': 'fixed',
                'SRC': node['uri']
            }
            self.body.pop()
            src = node['uri']
            if src.startswith('/'):
                src = join('content', src[1:])
                kwargs['width'], kwargs['height'] = PIL.Image.open(src).size
            matched = self.RE_IMAGE_CLASSES.search(last)
            if matched:
                kwargs['class'] = matched.groups()[0]
            self.body.append(self.starttag(node, 'amp-img', **kwargs).strip())
            self.body.append('</amp-img>')
        else:
            raise AssertionError("Why's there no <img> tag as last element on the stack?")

    def visit_citation(self, node):
        self.body.append(self.starttag(node, 'table', CLASS='docutils citation'))
        self.body.append('<colgroup><col class="label" /><col /></colgroup><tbody><tr>')
        self.footnote_backrefs(node)

    def depart_colspec(self, node):
        # write out <colgroup> when all colspecs are processed
        if isinstance(node.next_node(descend=False, siblings=True),
                      nodes.colspec):
            return
        if 'colwidths-auto' in node.parent.parent['classes'] or (
            'colwidths-auto' in self.settings.table_style and
            ('colwidths-given' not in node.parent.parent['classes'])):
            return
        self.body.append(self.starttag(node, 'colgroup'))
        for node in self.colspecs:
            self.body.append(self.emptytag(node, 'col'))
        self.body.append('</colgroup>\n')

    def visit_docinfo(self, node):
        self.context.append(len(self.body))
        self.body.append(self.starttag(node, 'table', CLASS='docinfo'))
        self.body.append('<col class="docinfo-name" /><col class="docinfo-content" /><tbody>')
        self.in_docinfo = True

    def visit_footnote(self, node):
        self.body.append(self.starttag(node, 'table', CLASS='docutils footnote'))
        self.body.append('<colgroup><col class="label" /><col /></colgroup><tbody><tr>')
        self.footnote_backrefs(node)

    def visit_field_list(self, node):
        super().visit_field_list(node)
        new_last = '<col class="field-name" /><col class="field-body" /><tbody>'
        self.body = self.body[:-1] + [new_last]

    def visit_option_list(self, node):
        self.body.append(self.starttag(node, 'table', CLASS='docutils option-list'))
        self.body.append('<col class="option" /><col class="description" /><tbody>')

    def visit_pngmath(self, node):
        src = node.attributes['src']
        kwargs = {
            'CLASS': 'pngmath',
            'LAYOUT': 'responsive',
            'SRC': src,
        }
        src = join('content', src[1:])
        kwargs['width'], kwargs['height'] = PIL.Image.open(src).size
        self.body.append(self.starttag(node, 'amp-img', **kwargs).strip())

    def depart_pngmath(self, node):
        self.body.append('</amp-img>')

    def visit_tbody(self, node):
        self.body.append(self.starttag(node, 'tbody'))

    def visit_thead(self, node):
        self.body.append(self.starttag(node, 'thead'))

    def visit_speakerdeck(self, node):
        # There's no support for speakerdeck in AMP so far
        pass

    def depart_speakerdeck(self, node):
        # There's no support for speakerdeck in AMP so far
        pass
