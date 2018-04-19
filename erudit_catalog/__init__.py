"""Just to ease the access to the files.
"""
import os


class Catalog:
    _CWD = os.path.dirname(os.path.abspath(__file__))

    NAME = 'Erudit Style Catalog for PackTooks'

    # Validation schemas: XSD or DTD files.
    SCH_SCHEMAS = {
        'eps-0.1': os.path.join(_CWD, 'erudit-style-0.1.sch'),
    }

    DTDS = {
        'JATS-journalpublishing1.dtd': os.path.join(
            _CWD, 'jats-publishing-dtd-1.0/JATS-journalpublishing1.dtd'),
        'journalpublishing3.dtd': os.path.join(
            _CWD, 'pmc-publishing-dtd-3.0/journalpublishing3.dtd'),
    }

    # Python>=3.5 is possible to use the syntax: SCHEMAS = {**SCH_SCHEMAS, **DTDS}
    # https://docs.python.org/dev/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations
    SCHEMAS = dict(SCH_SCHEMAS)
    SCHEMAS.update(DTDS)

    # XML Catalog - OASIS Standard.
    XML_CATALOG = os.path.join(_CWD, 'erudit-publishing-schema.xml')

    HTML_GEN_XSLTS = {
        'root-html-1.0.xslt': os.path.join(_CWD, 'htmlgenerator/root-html-1.0.xslt'),
    }
    HTML_GEN_DEFAULT_PRINT_CSS_PATH = os.path.join(_CWD, 'htmlgenerator/static/bundle-print.css')
    HTML_GEN_DEFAULT_CSS_PATH = os.path.join(_CWD, 'htmlgenerator/static/article-standalone.css')
    HTML_GEN_DEFAULT_JS_PATH = os.path.join(_CWD, 'htmlgenerator/static/article-standalone-min.js')

    # As a general rule, only the latest 2 versions are supported simultaneously.
    CURRENTLY_SUPPORTED_VERSIONS = os.environ.get(
        'PACKTOOLS_SUPPORTED_SPS_VERSIONS', 'eps-0.1').split(':')

    ALLOWED_PUBLIC_IDS = (
        '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
    )

    # doctype public ids for sps <= 1.1
    ALLOWED_PUBLIC_IDS_LEGACY = (
        '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
    )


catalog = Catalog()
