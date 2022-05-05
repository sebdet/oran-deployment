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
from onapsdk.exceptions import ResourceNotFound
from waiting import wait
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.policy.policy import OranPolicy, PolicyType
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env
from smo.network_simulators import NetworkSimulators
from smo.dmaap import DmaapUtils
from smo.cl_usecase import ClCommissioningUtils


# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Apex policy")
dmaap = OranDmaap()
dmaap_utils = DmaapUtils()
clcommissioning_utils = ClCommissioningUtils()
network_simulators = NetworkSimulators("./resources")
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)
policy = OranPolicy()
usecase_name = "apex_usecase"

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Prepare the test environment before the executing the tests."""
    logger.info("Test class setup for Closed Loop Apex test")

    dmaap_utils.clean_dmaap(settings.DMAAP_CL_GROUP, settings.DMAAP_CL_USER)

    network_simulators.start_and_wait_network_simulators()

    # Wait enough time to have at least the SDNR notifications sent
    logger.info("Waiting 10s that SDNR sends all registration events to VES...")
    time.sleep(10)
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    # Finish and delete the cl instance
    clcommissioning_utils.clean_instance(usecase_name)

    try:
        policy.undeploy_policy("operational.apex.linkmonitor", "1.0.0", settings.POLICY_BASICAUTH)
    except ResourceNotFound:
        logger.info("Policy already undeployed")
        try:
            policy.delete_policy(PolicyType(type="onap.policies.controlloop.operational.common.Apex", version="1.0.0"), "operational.apex.linkmonitor", "1.0.0", settings.POLICY_BASICAUTH)
        except ResourceNotFound:
            logger.info("Policy already deleted")

    network_simulators.stop_network_simulators()
    time.sleep(10)
    logger.info("Test Session cleanup done")

def verify_apex_policy_created():
    """
    Verify whether the Apex policy has deployed successfully.

    Returns:
        the boolean value indicating whether policy deployed successfully
    """
    logger.info("Verify Apex policy is deployed")
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)
    logger.info("policy_list: %s", policy_status_list)
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
    commissioning_payload = jinja_env().get_template("commission_apex.json.j2").render(dmaapGroup=settings.DMAAP_CL_GROUP, dmaapUser=settings.DMAAP_CL_USER)
    instance_payload = jinja_env().get_template("create_instance_apex.json.j2").render(dmaapGroup=settings.DMAAP_CL_GROUP, dmaapUser=settings.DMAAP_CL_USER, instanceName=usecase_name)
    assert clcommissioning_utils.create_instance(usecase_name, commissioning_payload, instance_payload) is True

    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"

    send_dmaap_event()

    wait(lambda: verify_apex_policy_created(), sleep_seconds=10, timeout_seconds=60, waiting_for="Policy Deployment to be OK")

    time.sleep(20)
    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"
