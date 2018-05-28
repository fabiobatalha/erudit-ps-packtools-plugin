#coding: utf-8
from __future__ import unicode_literals
import logging
import itertools
import json

import plumber

from packtools.style_errors import StyleError
from packtools.catalogs import catalog

LOGGER = logging.getLogger(__name__)

with open(catalog.ISO3166_CODES) as f:
    ISO3166_CODES_SET = set(json.load(f))


# --------------------------------
# Basic functionality
# --------------------------------
@plumber.filter
def setup(message):
    """Prepare the message to traverse the pipeline.

    The input `message` is an `etree` instance. The pipeline will inspect
    this etree and append the errors on an errors list. This errors list
    is instantiated at this setup pipe.
    """
    return message, []


@plumber.filter
def teardown(message):
    """Finalize the processing pipeline and return the errors list.
    """
    _, err_list = message
    return err_list


def StyleCheckingPipeline():
    """Factory for style checking pipelines.
    """
    return plumber.Pipeline(setup, doctype, country_code, teardown)


@plumber.filter
def doctype(message):
    """Make sure the DOCTYPE declaration is present.
    """
    et, err_list = message

    if not et.docinfo.doctype:
        err = StyleError()
        err.message = "Missing DOCTYPE declaration."
        err_list.append(err)

    return message


@plumber.filter
def country_code(message):
    """Check country codes against iso3166 alpha-2 list.
    """
    et, err_list = message

    elements = et.findall('//*[@country]')
    for elem in elements:
        value = elem.attrib['country']
        if value not in ISO3166_CODES_SET:
            err = StyleError()
            err.line = elem.sourceline
            err.message = "Element '%s', attribute country: Invalid country code \"%s\"." % (elem.tag, value)
            err_list.append(err)

    return message
