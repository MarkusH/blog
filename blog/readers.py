from docutils.core import Publisher
from docutils.io import StringOutput
from pelican.readers import RstReader

from .translators import BlogHTMLTranslator


class BlogReader(RstReader):
    enabled = True

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
