"""
    sphinx.builders.latex
    ~~~~~~~~~~~~~~~~~~~~~

    LaTeX builder.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os
import warnings
from os import path
from typing import Any, Dict, Iterable, List, Tuple, Union

from docutils.frontend import OptionParser
from docutils.nodes import Node

import sphinx.builders.latex.nodes  # NOQA  # Workaround: import this before writer to avoid ImportError
from sphinx import addnodes, highlighting, package_dir
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.latex.constants import ADDITIONAL_SETTINGS, DEFAULT_SETTINGS, SHORTHANDOFF
from sphinx.builders.latex.theming import Theme, ThemeFactory
from sphinx.builders.latex.util import ExtBabel
from sphinx.config import ENUM, Config
from sphinx.deprecation import RemovedInSphinx40Warning, RemovedInSphinx50Warning
from sphinx.environment.adapters.asset import ImageAdapter
from sphinx.errors import NoUri, SphinxError
from sphinx.locale import _, __
from sphinx.util import logging, progress_message, status_iterator, texescape
from sphinx.util.console import bold, darkgreen  # type: ignore
from sphinx.util.docutils import SphinxFileOutput, new_document
from sphinx.util.fileutil import copy_asset_file
from sphinx.util.i18n import format_date
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import SEP, make_filename_from_project
from sphinx.util.template import LaTeXRenderer
from sphinx.writers.latex import LaTeXTranslator, LaTeXWriter

# load docutils.nodes after loading sphinx.builders.latex.nodes
from docutils import nodes  # isort:skip

XINDY_LANG_OPTIONS = {
    # language codes from docutils.writers.latex2e.Babel
    # ! xindy language names may differ from those in use by LaTeX/babel
    # ! xindy does not support all Latin scripts as recognized by LaTeX/babel
    # ! not all xindy-supported languages appear in Babel.language_codes
    # cd /usr/local/texlive/2018/texmf-dist/xindy/modules/lang
    # find . -name '*utf8.xdy'
    # LATIN
    'sq': '-L albanian -C utf8 ',
    'hr': '-L croatian -C utf8 ',
    'cs': '-L czech -C utf8 ',
    'da': '-L danish -C utf8 ',
    'nl': '-L dutch-ij-as-ij -C utf8 ',
    'en': '-L english -C utf8 ',
    'eo': '-L esperanto -C utf8 ',
    'et': '-L estonian -C utf8 ',
    'fi': '-L finnish -C utf8 ',
    'fr': '-L french -C utf8 ',
    'de': '-L german-din5007 -C utf8 ',
    'is': '-L icelandic -C utf8 ',
    'it': '-L italian -C utf8 ',
    'la': '-L latin -C utf8 ',
    'lv': '-L latvian -C utf8 ',
    'lt': '-L lithuanian -C utf8 ',
    'dsb': '-L lower-sorbian -C utf8 ',
    'ds': '-L lower-sorbian -C utf8 ',   # trick, no conflict
    'nb': '-L norwegian -C utf8 ',
    'no': '-L norwegian -C utf8 ',       # and what about nynorsk?
    'pl': '-L polish -C utf8 ',
    'pt': '-L portuguese -C utf8 ',
    'ro': '-L romanian -C utf8 ',
    'sk': '-L slovak-small -C utf8 ',    # there is also slovak-large
    'sl': '-L slovenian -C utf8 ',
    'es': '-L spanish-modern -C utf8 ',  # there is also spanish-traditional
    'sv': '-L swedish -C utf8 ',
    'tr': '-L turkish -C utf8 ',
    'hsb': '-L upper-sorbian -C utf8 ',
    'hs': '-L upper-sorbian -C utf8 ',   # trick, no conflict
    'vi': '-L vietnamese -C utf8 ',
    # CYRILLIC
    # for usage with pdflatex, needs also cyrLICRutf8.xdy module
    'be': '-L belarusian -C utf8 ',
    'bg': '-L bulgarian -C utf8 ',
    'mk': '-L macedonian -C utf8 ',
    'mn': '-L mongolian-cyrillic -C utf8 ',
    'ru': '-L russian -C utf8 ',
    'sr': '-L serbian -C utf8 ',
    'sh-cyrl': '-L serbian -C utf8 ',
    'sh': '-L serbian -C utf8 ',         # trick, no conflict
    'uk': '-L ukrainian -C utf8 ',
    # GREEK
    # can work only with xelatex/lualatex, not supported by texindy+pdflatex
    'el': '-L greek -C utf8 ',
    # FIXME, not compatible with [:2] slice but does Sphinx support Greek ?
    'el-polyton': '-L greek-polytonic -C utf8 ',
}

XINDY_CYRILLIC_SCRIPTS = [
    'be', 'bg', 'mk', 'mn', 'ru', 'sr', 'sh', 'uk',
]

logger = logging.getLogger(__name__)


class LaTeXBuilder(Builder):
    """
    Builds LaTeX output to create PDF.
    """
    name = 'latex'
    format = 'latex'
    epilog = __('The LaTeX files are in %(outdir)s.')
    if os.name == 'posix':
        epilog += __("\nRun 'make' in that directory to run these through "
                     "(pdf)latex\n"
                     "(use `make latexpdf' here to do that automatically).")

    supported_image_types = ['application/pdf', 'image/png', 'image/jpeg']
    supported_remote_images = False
    default_translator_class = LaTeXTranslator

    def init(self) -> None:
        self.babel = None           # type: ExtBabel
        self.context = {}           # type: Dict[str, Any]
        self.docnames = []          # type: Iterable[str]
        self.document_data = []     # type: List[Tuple[str, str, str, str, str, bool]]
        self.themes = ThemeFactory(self.app)
        texescape.init()

        self.init_context()
        self.init_babel()
        self.init_multilingual()

    def get_outdated_docs(self) -> Union[str, List[str]]:
        return 'all documents'  # for now

    def get_target_uri(self, docname: str, typ: str = None) -> str:
        if docname not in self.docnames:
            raise NoUri(docname, typ)
        else:
            return '%' + docname

    def get_relative_uri(self, from_: str, to: str, typ: str = None) -> str:
        # ignore source path
        return self.get_target_uri(to, typ)

    def init_document_data(self) -> None:
        preliminary_document_data = [list(x) for x in self.config.latex_documents]
        if not preliminary_document_data:
            logger.warning(__('no "latex_documents" config value found; no documents '
                              'will be written'))
            return
        # assign subdirs to titles
        self.titles = []  # type: List[Tuple[str, str]]
        for entry in preliminary_document_data:
            docname = entry[0]
            if docname not in self.env.all_docs:
                logger.warning(__('"latex_documents" config value references unknown '
                                  'document %s'), docname)
                continue
            self.document_data.append(entry)  # type: ignore
            if docname.endswith(SEP + 'index'):
                docname = docname[:-5]
            self.titles.append((docname, entry[2]))

    def init_context(self) -> None:
        self.context = DEFAULT_SETTINGS.copy()

        # Add special settings for latex_engine
        self.context.update(ADDITIONAL_SETTINGS.get(self.config.latex_engine, {}))

        # Add special settings for (latex_engine, language_code)
        if self.config.language:
            key = (self.config.latex_engine, self.config.language[:2])
            self.context.update(ADDITIONAL_SETTINGS.get(key, {}))

        # Apply user settings to context
        self.context.update(self.config.latex_elements)
        self.context['release'] = self.config.release
        self.context['use_xindy'] = self.config.latex_use_xindy

        if self.config.today:
            self.context['date'] = self.config.today
        else:
            self.context['date'] = format_date(self.config.today_fmt or _('%b %d, %Y'),
                                               language=self.config.language)

        if self.config.latex_logo:
            self.context['logofilename'] = path.basename(self.config.latex_logo)

        # for compatibilities
        self.context['indexname'] = _('Index')
        if self.config.release:
            # Show the release label only if release value exists
            self.context.setdefault('releasename', _('Release'))

    def update_context(self) -> None:
        """Update template variables for .tex file just before writing."""
        # Apply extension settings to context
        registry = self.app.registry
        self.context['packages'] = registry.latex_packages
        self.context['packages_after_hyperref'] = registry.latex_packages_after_hyperref

    def init_babel(self) -> None:
        self.babel = ExtBabel(self.config.language, not self.context['babel'])
        if self.config.language and not self.babel.is_supported_language():
            # emit warning if specified language is invalid
            # (only emitting, nothing changed to processing)
            logger.warning(__('no Babel option known for language %r'),
                           self.config.language)

    def init_multilingual(self) -> None:
        if self.context['latex_engine'] == 'pdflatex':
            if not self.babel.uses_cyrillic():
                if 'X2' in self.context['fontenc']:
                    self.context['substitutefont'] = '\\usepackage{substitutefont}'
                    self.context['textcyrillic'] = '\\usepackage[Xtwo]{sphinxcyrillic}'
                elif 'T2A' in self.context['fontenc']:
                    self.context['substitutefont'] = '\\usepackage{substitutefont}'
                    self.context['textcyrillic'] = '\\usepackage[TtwoA]{sphinxcyrillic}'
            if 'LGR' in self.context['fontenc']:
                self.context['substitutefont'] = '\\usepackage{substitutefont}'
            else:
                self.context['textgreek'] = ''

        # 'babel' key is public and user setting must be obeyed
        if self.context['babel']:
            self.context['classoptions'] += ',' + self.babel.get_language()
            # this branch is not taken for xelatex/lualatex if default settings
            self.context['multilingual'] = self.context['babel']
            if self.config.language:
                self.context['shorthandoff'] = SHORTHANDOFF

                # Times fonts don't work with Cyrillic languages
                if self.babel.uses_cyrillic() and 'fontpkg' not in self.config.latex_elements:
                    self.context['fontpkg'] = ''
        elif self.context['polyglossia']:
            self.context['classoptions'] += ',' + self.babel.get_language()
            options = self.babel.get_mainlanguage_options()
            if options:
                language = r'\setmainlanguage[%s]{%s}' % (options, self.babel.get_language())
            else:
                language = r'\setmainlanguage{%s}' % self.babel.get_language()

            self.context['multilingual'] = '%s\n%s' % (self.context['polyglossia'], language)

    def write_stylesheet(self) -> None:
        highlighter = highlighting.PygmentsBridge('latex', self.config.pygments_style)
        stylesheet = path.join(self.outdir, 'sphinxhighlight.sty')
        with open(stylesheet, 'w') as f:
            f.write('\\NeedsTeXFormat{LaTeX2e}[1995/12/01]\n')
            f.write('\\ProvidesPackage{sphinxhighlight}'
                    '[2016/05/29 stylesheet for highlighting with pygments]\n\n')
            f.write(highlighter.get_stylesheet())

    def write(self, *ignored: Any) -> None:
        docwriter = LaTeXWriter(self)
        docsettings = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,),
            read_config_files=True).get_default_values()  # type: Any
        patch_settings(docsettings)

        self.init_document_data()
        self.write_stylesheet()

        for entry in self.document_data:
            docname, targetname, title, author, themename = entry[:5]
            theme = self.themes.get(themename)
            toctree_only = False
            if len(entry) > 5:
                toctree_only = entry[5]
            destination = SphinxFileOutput(destination_path=path.join(self.outdir, targetname),
                                           encoding='utf-8', overwrite_if_changed=True)
            with progress_message(__("processing %s") % targetname):
                doctree = self.env.get_doctree(docname)
                toctree = next(iter(doctree.traverse(addnodes.toctree)), None)
                if toctree and toctree.get('maxdepth') > 0:
                    tocdepth = toctree.get('maxdepth')
                else:
                    tocdepth = None

                doctree = self.assemble_doctree(
                    docname, toctree_only,
                    appendices=(self.config.latex_appendices if theme.name != 'howto' else []))
                doctree['docclass'] = theme.docclass
                doctree['contentsname'] = self.get_contentsname(docname)
                doctree['tocdepth'] = tocdepth
                self.post_process_images(doctree)
                self.update_doc_context(title, author, theme)
                self.update_context()

            with progress_message(__("writing")):
                docsettings._author = author
                docsettings._title = title
                docsettings._contentsname = doctree['contentsname']
                docsettings._docname = docname
                docsettings._docclass = theme.name

                doctree.settings = docsettings
                docwriter.theme = theme
                docwriter.write(doctree, destination)

    def get_contentsname(self, indexfile: str) -> str:
        tree = self.env.get_doctree(indexfile)
        contentsname = None
        for toctree in tree.traverse(addnodes.toctree):
            if 'caption' in toctree:
                contentsname = toctree['caption']
                break

        return contentsname

    def update_doc_context(self, title: str, author: str, theme: Theme) -> None:
        self.context['title'] = title
        self.context['author'] = author
        self.context['docclass'] = theme.docclass
        self.context['papersize'] = theme.papersize
        self.context['pointsize'] = theme.pointsize
        self.context['wrapperclass'] = theme.wrapperclass

    def assemble_doctree(self, indexfile: str, toctree_only: bool, appendices: List[str]) -> nodes.document:  # NOQA
        self.docnames = set([indexfile] + appendices)
        logger.info(darkgreen(indexfile) + " ", nonl=True)
        tree = self.env.get_doctree(indexfile)
        tree['docname'] = indexfile
        if toctree_only:
            # extract toctree nodes from the tree and put them in a
            # fresh document
            new_tree = new_document('<latex output>')
            new_sect = nodes.section()
            new_sect += nodes.title('<Set title in conf.py>',
                                    '<Set title in conf.py>')
            new_tree += new_sect
            for node in tree.traverse(addnodes.toctree):
                new_sect += node
            tree = new_tree
        largetree = inline_all_toctrees(self, self.docnames, indexfile, tree,
                                        darkgreen, [indexfile])
        largetree['docname'] = indexfile
        for docname in appendices:
            appendix = self.env.get_doctree(docname)
            appendix['docname'] = docname
            largetree.append(appendix)
        logger.info('')
        logger.info(__("resolving references..."))
        self.env.resolve_references(largetree, indexfile, self)
        # resolve :ref:s to distant tex files -- we can't add a cross-reference,
        # but append the document name
        for pendingnode in largetree.traverse(addnodes.pending_xref):
            docname = pendingnode['refdocname']
            sectname = pendingnode['refsectname']
            newnodes = [nodes.emphasis(sectname, sectname)]  # type: List[Node]
            for subdir, title in self.titles:
                if docname.startswith(subdir):
                    newnodes.append(nodes.Text(_(' (in '), _(' (in ')))
                    newnodes.append(nodes.emphasis(title, title))
                    newnodes.append(nodes.Text(')', ')'))
                    break
            else:
                pass
            pendingnode.replace_self(newnodes)
        return largetree

    def apply_transforms(self, doctree: nodes.document) -> None:
        warnings.warn('LaTeXBuilder.apply_transforms() is deprecated.',
                      RemovedInSphinx40Warning, stacklevel=2)

    def finish(self) -> None:
        self.copy_image_files()
        self.write_message_catalog()
        self.copy_support_files()

        if self.config.latex_additional_files:
            self.copy_latex_additional_files()

    @progress_message(__('copying TeX support files'))
    def copy_support_files(self) -> None:
        """copy TeX support files from texinputs."""
        # configure usage of xindy (impacts Makefile and latexmkrc)
        # FIXME: convert this rather to a confval with suitable default
        #        according to language ? but would require extra documentation
        if self.config.language:
            xindy_lang_option = \
                XINDY_LANG_OPTIONS.get(self.config.language[:2],
                                       '-L general -C utf8 ')
            xindy_cyrillic = self.config.language[:2] in XINDY_CYRILLIC_SCRIPTS
        else:
            xindy_lang_option = '-L english -C utf8 '
            xindy_cyrillic = False
        context = {
            'latex_engine':      self.config.latex_engine,
            'xindy_use':         self.config.latex_use_xindy,
            'xindy_lang_option': xindy_lang_option,
            'xindy_cyrillic':    xindy_cyrillic,
        }
        logger.info(bold(__('copying TeX support files...')))
        staticdirname = path.join(package_dir, 'texinputs')
        for filename in os.listdir(staticdirname):
            if not filename.startswith('.'):
                copy_asset_file(path.join(staticdirname, filename),
                                self.outdir, context=context)

        # use pre-1.6.x Makefile for make latexpdf on Windows
        if os.name == 'nt':
            staticdirname = path.join(package_dir, 'texinputs_win')
            copy_asset_file(path.join(staticdirname, 'Makefile_t'),
                            self.outdir, context=context)

    @progress_message(__('copying additional files'))
    def copy_latex_additional_files(self) -> None:
        for filename in self.config.latex_additional_files:
            logger.info(' ' + filename, nonl=True)
            copy_asset_file(path.join(self.confdir, filename), self.outdir)

    def copy_image_files(self) -> None:
        if self.images:
            stringify_func = ImageAdapter(self.app.env).get_original_image_uri
            for src in status_iterator(self.images, __('copying images... '), "brown",
                                       len(self.images), self.app.verbosity,
                                       stringify_func=stringify_func):
                dest = self.images[src]
                try:
                    copy_asset_file(path.join(self.srcdir, src),
                                    path.join(self.outdir, dest))
                except Exception as err:
                    logger.warning(__('cannot copy image file %r: %s'),
                                   path.join(self.srcdir, src), err)
        if self.config.latex_logo:
            if not path.isfile(path.join(self.confdir, self.config.latex_logo)):
                raise SphinxError(__('logo file %r does not exist') % self.config.latex_logo)
            else:
                copy_asset_file(path.join(self.confdir, self.config.latex_logo), self.outdir)

    def write_message_catalog(self) -> None:
        formats = self.config.numfig_format
        context = {
            'addtocaptions': r'\@iden',
            'figurename': formats.get('figure', '').split('%s', 1),
            'tablename': formats.get('table', '').split('%s', 1),
            'literalblockname': formats.get('code-block', '').split('%s', 1)
        }

        if self.context['babel'] or self.context['polyglossia']:
            context['addtocaptions'] = r'\addto\captions%s' % self.babel.get_language()

        filename = path.join(package_dir, 'templates', 'latex', 'sphinxmessages.sty_t')
        copy_asset_file(filename, self.outdir, context=context, renderer=LaTeXRenderer())

    @property
    def usepackages(self) -> List[Tuple[str, str]]:
        warnings.warn('LaTeXBuilder.usepackages is deprecated.',
                      RemovedInSphinx50Warning, stacklevel=2)
        return self.app.registry.latex_packages

    @property
    def usepackages_after_hyperref(self) -> List[Tuple[str, str]]:
        warnings.warn('LaTeXBuilder.usepackages_after_hyperref is deprecated.',
                      RemovedInSphinx50Warning, stacklevel=2)
        return self.app.registry.latex_packages_after_hyperref


def patch_settings(settings: Any) -> Any:
    """Make settings object to show deprecation messages."""

    class Values(type(settings)):  # type: ignore
        @property
        def author(self) -> str:
            warnings.warn('settings.author is deprecated',
                          RemovedInSphinx40Warning, stacklevel=2)
            return self._author

        @property
        def title(self) -> str:
            warnings.warn('settings.title is deprecated',
                          RemovedInSphinx40Warning, stacklevel=2)
            return self._title

        @property
        def contentsname(self) -> str:
            warnings.warn('settings.contentsname is deprecated',
                          RemovedInSphinx40Warning, stacklevel=2)
            return self._contentsname

        @property
        def docname(self) -> str:
            warnings.warn('settings.docname is deprecated',
                          RemovedInSphinx40Warning, stacklevel=2)
            return self._docname

        @property
        def docclass(self) -> str:
            warnings.warn('settings.docclass is deprecated',
                          RemovedInSphinx40Warning, stacklevel=2)
            return self._docclass

    # dynamic subclassing
    settings.__class__ = Values


def validate_config_values(app: Sphinx, config: Config) -> None:
    for key in list(config.latex_elements):
        if key not in DEFAULT_SETTINGS:
            msg = __("Unknown configure key: latex_elements[%r], ignored.")
            logger.warning(msg % (key,))
            config.latex_elements.pop(key)


def validate_latex_theme_options(app: Sphinx, config: Config) -> None:
    for key in list(config.latex_theme_options):
        if key not in Theme.UPDATABLE_KEYS:
            msg = __("Unknown theme option: latex_theme_options[%r], ignored.")
            logger.warning(msg % (key,))
            config.latex_theme_options.pop(key)


def install_packages_for_ja(app: Sphinx) -> None:
    """Install packages for Japanese."""
    if app.config.language == 'ja' and app.config.latex_engine in ('platex', 'uplatex'):
        app.add_latex_package('pxjahyper', after_hyperref=True)


def default_latex_engine(config: Config) -> str:
    """ Better default latex_engine settings for specific languages. """
    if config.language == 'ja':
        return 'platex'
    elif (config.language or '').startswith('zh'):
        return 'xelatex'
    elif config.language == 'el':
        return 'xelatex'
    else:
        return 'pdflatex'


def default_latex_docclass(config: Config) -> Dict[str, str]:
    """ Better default latex_docclass settings for specific languages. """
    if config.language == 'ja':
        if config.latex_engine == 'uplatex':
            return {'manual': 'ujbook',
                    'howto': 'ujreport'}
        else:
            return {'manual': 'jsbook',
                    'howto': 'jreport'}
    else:
        return {}


def default_latex_use_xindy(config: Config) -> bool:
    """ Better default latex_use_xindy settings for specific engines. """
    return config.latex_engine in {'xelatex', 'lualatex'}


def default_latex_documents(config: Config) -> List[Tuple[str, str, str, str, str]]:
    """ Better default latex_documents settings. """
    project = texescape.escape(config.project, config.latex_engine)
    author = texescape.escape(config.author, config.latex_engine)
    return [(config.master_doc,
             make_filename_from_project(config.project) + '.tex',
             texescape.escape_abbr(project),
             texescape.escape_abbr(author),
             config.latex_theme)]


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension('sphinx.builders.latex.transforms')

    app.add_builder(LaTeXBuilder)
    app.connect('config-inited', validate_config_values, priority=800)
    app.connect('config-inited', validate_latex_theme_options, priority=800)
    app.connect('builder-inited', install_packages_for_ja)

    app.add_config_value('latex_engine', default_latex_engine, None,
                         ENUM('pdflatex', 'xelatex', 'lualatex', 'platex', 'uplatex'))
    app.add_config_value('latex_documents', default_latex_documents, None)
    app.add_config_value('latex_logo', None, None, [str])
    app.add_config_value('latex_appendices', [], None)
    app.add_config_value('latex_use_latex_multicolumn', False, None)
    app.add_config_value('latex_use_xindy', default_latex_use_xindy, None, [bool])
    app.add_config_value('latex_toplevel_sectioning', None, None,
                         ENUM(None, 'part', 'chapter', 'section'))
    app.add_config_value('latex_domain_indices', True, None, [list])
    app.add_config_value('latex_show_urls', 'no', None)
    app.add_config_value('latex_show_pagerefs', False, None)
    app.add_config_value('latex_elements', {}, None)
    app.add_config_value('latex_additional_files', [], None)
    app.add_config_value('latex_theme', 'manual', None, [str])
    app.add_config_value('latex_theme_options', {}, None)
    app.add_config_value('latex_theme_path', [], None, [list])

    app.add_config_value('latex_docclass', default_latex_docclass, None)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
