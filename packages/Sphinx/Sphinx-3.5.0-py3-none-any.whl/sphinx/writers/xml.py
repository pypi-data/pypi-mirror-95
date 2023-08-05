"""
    sphinx.writers.xml
    ~~~~~~~~~~~~~~~~~~

    Docutils-native XML and pseudo-XML writers.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from typing import Any

from docutils.writers.docutils_xml import Writer as BaseXMLWriter

from sphinx.builders import Builder


class XMLWriter(BaseXMLWriter):
    def __init__(self, builder: Builder) -> None:
        super().__init__()
        self.builder = builder
        self.translator_class = self.builder.get_translator_class()

    def translate(self, *args: Any, **kwargs: Any) -> None:
        self.document.settings.newlines = \
            self.document.settings.indents = \
            self.builder.env.config.xml_pretty
        self.document.settings.xml_declaration = True
        self.document.settings.doctype_declaration = True
        return super().translate()


class PseudoXMLWriter(BaseXMLWriter):

    supported = ('pprint', 'pformat', 'pseudoxml')
    """Formats this writer supports."""

    config_section = 'pseudoxml writer'
    config_section_dependencies = ('writers',)

    output = None
    """Final translated form of `document`."""

    def __init__(self, builder: Builder) -> None:
        super().__init__()
        self.builder = builder

    def translate(self) -> None:
        self.output = self.document.pformat()

    def supports(self, format: str) -> bool:
        """This writer supports all format-specific elements."""
        return True
