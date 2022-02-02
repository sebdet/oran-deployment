#!/usr/bin/env python3
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

"""A1Sim tests module."""
import logging
from onapsdk.configuration import settings
from oransdk.a1sim.a1sim import A1sim
from oransdk.utils.jinja import jinja_env

BASIC_AUTH = {}

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test DMAAP")

def test_a1sim():
    """Test the A1 sims."""
    logger.info("Get ric version for ost")
    a1sim = A1sim()
    a1sim.check_version(settings.A1SIM_OSC_URL)
    a1sim.check_status(settings.A1SIM_OSC_URL)
    a1sim.get_policy_number(settings.A1SIM_OSC_URL)

    data = jinja_env().get_template("OSC/policy_type.json.j2").render()
    a1sim.create_policy_type(settings.A1SIM_OSC_URL, 1, data)
