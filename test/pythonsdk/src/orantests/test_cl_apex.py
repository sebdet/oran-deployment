#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2022 AT&T Intellectual Property. All rights
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
"""Closed Loop Apex usecase tests module."""

import time

import logging
import logging.config
import os
import pytest
from onapsdk.configuration import settings
from waiting import wait
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.policy.policy import OranPolicy
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env
from smo.network_simulators import NetworkSimulators
from smo.dmaap import DmaapUtils

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Apex policy")
dmaap = OranDmaap()
dmaap_utils = DmaapUtils()
network_simulators = NetworkSimulators("./resources")
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Setup the simulators before the executing the tests."""
    logger.info("Test class setup for Closed Loop Apex test")

    dmaap_utils.clean_dmaap()

    network_simulators.start_and_wait_network_simulators()

    # Wait enough time to have at least the SDNR notifications sent
    logger.info("Waiting 10s that SDNR sends all registration events to VES...")
    time.sleep(10)
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    clamp.change_instance_status("PASSIVE", "PMSH_Instance1", "1.2.3")
    wait(lambda: clamp.verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to PASSIVE")
    clamp.change_instance_status("UNINITIALISED", "PMSH_Instance1", "1.2.3")
    wait(lambda: clamp.verify_instance_status("UNINITIALISED"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to UNINITIALISED")

    logger.info("Delete Instance")
    clamp.delete_template_instance("PMSH_Instance1", "1.2.3")
    logger.info("Decommission tosca")
    clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")
    network_simulators.stop_network_simulators()
    logger.info("Test Session cleanup done")

def verify_apex_policy_created():
    """
    Verify whether the Apex policy has deployed successfully.

    Returns:
        the boolean value indicating whether policy deployed successfully
    """
    logger.info("Verify Apex policy is deployed")
    policy = OranPolicy()
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)

    for status in policy_status_list:
        logger.info("the status %s,%s,%s,%s:", status["policy"]["name"], status["policy"]["version"], status["deploy"], status["state"])
        if (status["policy"]["name"] == "operational.apex.linkmonitor" and status["policy"]["version"] == "1.0.0" and status["deploy"] and status["state"] == "SUCCESS"):
            logger.info("Policy deployement OK")
            return True

    logger.info("Failed to deploy Apex policy")
    return False

def send_dmaap_event():
    """Send a event to Dmaap that should trigger the apex policy."""
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    dmaap.send_link_failure_event(event)

def test_cl_apex():
    """The Closed Loop O-RU Fronthaul Recovery usecase Apex version."""
    logger.info("Upload tosca to commissioning")
    tosca_template = jinja_env().get_template("commission_apex.json.j2").render(dmaapGroup=settings.DMAAP_GROUP, dmaapUser=settings.DMAAP_USER)
    response = clamp.upload_commission(tosca_template)
    assert response["errorDetails"] is None

    logger.info("Create Instance")
    response = clamp.create_instance(tosca_template)
    assert response["errorDetails"] is None

    logger.info("Change Instance Status to PASSIVE")
    response = clamp.change_instance_status("PASSIVE", "PMSH_Instance1", "1.2.3")
    wait(lambda: clamp.verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to PASSIVE")

    logger.info("Change Instance Status to RUNNING")
    response = clamp.change_instance_status("RUNNING", "PMSH_Instance1", "1.2.3")
    wait(lambda: clamp.verify_instance_status("RUNNING"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to RUNNING")

    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"

    send_dmaap_event()

    wait(lambda: verify_apex_policy_created(), sleep_seconds=10, timeout_seconds=60, waiting_for="Policy Deployment to be OK")

    time.sleep(20)
    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"
