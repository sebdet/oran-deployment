# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Jinja module."""

from jinja2 import Environment, PackageLoader, select_autoescape, ChoiceLoader


def jinja_env() -> Environment:
    """Create Jinja environment.

    jinja_env allow to fetch simply jinja templates where they are.
    by default jinja engine will look for templates in `templates` directory of
    the package. So to load a template, you just have to do:

    Example:
    >>> template = jinja_env().get_template('vendor_create.json.j2')
    >>> data = template.render(name="vendor")

    See also:
        SdcElement.create() for real use

    Returns:
        Environment: the Jinja environment to use

    """
    return Environment(autoescape=select_autoescape(['html', 'htm', 'xml']),
                       loader=ChoiceLoader([
                           PackageLoader("oransdk.a1sim"),
                           PackageLoader("oransdk.dmaap"),
                           PackageLoader("oransdk.enrichmentservice"),
                           PackageLoader("oransdk.policy")
                       ]))
