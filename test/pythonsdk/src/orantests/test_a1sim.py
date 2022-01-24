#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

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
