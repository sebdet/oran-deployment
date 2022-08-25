###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2021-2022 AT&T Intellectual Property. All rights
#                             reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END============================================
# ===================================================================
#
###
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
                           PackageLoader("oransdk.aai"),
                           PackageLoader("oransdk.dmaap"),
                           PackageLoader("oransdk.enrichmentservice"),
                           PackageLoader("oransdk.policy"),
                           PackageLoader("oransdk.sdc")
                       ]))
