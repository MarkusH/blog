from io import StringIO

from docutils.core import Publisher
from docutils.io import StringOutput
from pelican.readers import RstReader

from .translators import AMPTranslator, BlogHTMLTranslator


class AMPString(str):
    @property
    def amp_data(self):
        return self._amp_data

    @amp_data.setter
    def amp_data(self, value):
        self._amp_data = value


class BlogReader(RstReader):
    enabled = True

    def _get_publisher(self, source_path, translator_class=BlogHTMLTranslator):
        extra_params = {
            "initial_header_level": "2",
            "syntax_highlight": "short",
            "input_encoding": "utf-8",
            "exit_status_level": 2,
            "language_code": self._language_code,
            "halt_level": 2,
            "traceback": True,
            "warning_stream": StringIO(),
            "embed_stylesheet": False,
        }
        user_params = self.settings.get("DOCUTILS_SETTINGS")
        if user_params:
            extra_params.update(user_params)

        pub = Publisher(writer=self.writer_class(), destination_class=StringOutput)
        pub.set_components("standalone", "restructuredtext", "html")
        pub.writer.translator_class = translator_class
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish()
        return pub

    def read(self, source_path):
        content, metadata = super().read(source_path)
        content = AMPString(content)

        pub = self._get_publisher(source_path, AMPTranslator)
        parts = pub.writer.parts
        content.amp_data = parts.get("body")

        return content, metadata
