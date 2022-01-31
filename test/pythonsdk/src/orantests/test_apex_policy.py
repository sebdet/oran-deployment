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
"""Apex policy tests module."""
import time
import subprocess
import logging
import logging.config
import os
import pytest
from waiting import wait
from smo.network_simulators import NetworkSimulators
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy, PolicyType
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test APEX policy")
dmaap = OranDmaap()
policy = OranPolicy()
network_simulators = NetworkSimulators("./resources")

TOPIC_FAULT = '{"topicName": "unauthenticated.SEC_FAULT_OUTPUT"}'

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Setup the simulators before the executing the tests."""
    logger.info("Test class setup for Apex tests")

    dmaap.create_topic(TOPIC_FAULT)
    # Purge the FAULT TOPIC
    wait(lambda: (dmaap.get_message_from_topic("unauthenticated.SEC_FAULT_OUTPUT", 5000, settings.DMAAP_GROUP, settings.DMAAP_USER).json() == []), sleep_seconds=10, timeout_seconds=60, waiting_for="DMaap topic unauthenticated.SEC_FAULT_OUTPUT to be empty")

    network_simulators.start_network_simulators()
    network_simulators.wait_for_network_simulators_to_be_running()

    # Wait enough time to have at least the SDNR notifications sent
    logger.info("Waiting 10s that SDNR sends all registration events to VES...")
    time.sleep(10)
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    network_simulators.stop_network_simulators()
    logger.info("Test Session cleanup done")

def create_policy():
    """Create the policy."""
    logger.info("Create policy")
    policy_data = jinja_env().get_template("ToscaPolicy.json.j2").render()
    policy.create_policy(PolicyType(type="onap.policies.native.Apex", version="1.0.0"), policy_data, settings.POLICY_BASICAUTH)

    logger.info("Verify whether policy created successfully")
    assert policy.get_policy(PolicyType(type="onap.policies.native.Apex", version="1.0.0"), "onap.policies.native.apex.LinkMonitor", "1.0.0", settings.POLICY_BASICAUTH)

def deploy_policy():
    """Deploy the policy."""
    logger.info("Deploy policy")
    policy_to_deploy = jinja_env().get_template("DeployPolicyPAP.json.j2").render()
    policy.deploy_policy(policy_to_deploy, settings.POLICY_BASICAUTH)

    logger.info("Verify the policy is deployed")
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)
    policy_deployed = False
    for status in policy_status_list:
        logger.info("the status %s,%s,%s:", status["policy"]["name"], status["policy"]["version"], status["deploy"])
        if (status["policy"]["name"] == "onap.policies.native.apex.LinkMonitor" and status["policy"]["version"] == "1.0.0" and status["deploy"]):
            policy_deployed = True
            break

    assert policy_deployed

def policy_log_detected():
    logger.info("Wait for a while for Apex engine to be ready before sending Dmaap event")
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    dmaap.send_link_failure_event(event)
    if int(subprocess.getoutput('kubectl logs onap-policy-apex-pdp-0 -n onap | grep "Task Selection Execution: \'LinkMonitorPolicy:0.0.1:NULL:LinkFailureOrClearedState\'" | wc -l')) > 0:
        logger.info("Apex engine is ready. LinkFailureEvent sent to Dmaap")
        return True
    return False

def check_sdnc():
    """Verify that apex has changed the sdnc status."""
    logger.info("Check O-du/O-ru status")
    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"

    wait(lambda: policy_log_detected(), sleep_seconds=10, timeout_seconds=60, waiting_for="Policy apex log")

    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"

def test_apex_policy():
    """Test the apex policy."""
    create_policy()
    deploy_policy()
    check_sdnc()
