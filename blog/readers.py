from docutils import nodes
from docutils.core import Publisher
from docutils.io import StringOutput
from pelican.readers import RstReader, render_node_to_html

from .translators import BlogHTMLTranslator


class BlogReader(RstReader):
    enabled = True

    def _parse_metadata(self, document):
        """Return the dict containing document metadata"""
        output = {}
        for docinfo in document.traverse(nodes.docinfo):
            for element in docinfo.children:
                if element.tagname == 'field':  # custom fields (e.g. summary)
                    name_elem, body_elem = element.children
                    name = name_elem.astext()
                    if name in ('summary', 'image_credits'):
                        value = render_node_to_html(document, body_elem)
                    else:
                        value = body_elem.astext()
                elif element.tagname == 'authors':  # author list
                    name = element.tagname
                    value = [element.astext() for element in element.children]
                    value = ','.join(value)  # METADATA_PROCESSORS expects a string
                else:  # standard fields (e.g. address)
                    name = element.tagname
                    value = element.astext()
                name = name.lower()

                output[name] = self.process_metadata(name, value)
        return output

    def _get_publisher(self, source_path):
        extra_params = {
            'initial_header_level': '2',
            'syntax_highlight': 'short',
            'input_encoding': 'utf-8',
            'exit_status_level': 2,
            'embed_stylesheet': False
        }
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = Publisher(
            source_class=self.FileInput,
            destination_class=StringOutput
        )
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = BlogHTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish(enable_exit_status=True)
        return pub
