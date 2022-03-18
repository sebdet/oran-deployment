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
import logging
import logging.config
import os
import pytest
from waiting import wait
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy, PolicyType
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env
from smo.dmaap import DmaapUtils
from smo.network_simulators import NetworkSimulators

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test APEX policy")
dmaap = OranDmaap()
dmaap_utils = DmaapUtils()
policy = OranPolicy()
network_simulators = NetworkSimulators("./resources")

policy_id = "onap.policies.native.apex.LinkMonitor"
policy_version = "1.0.0"
policy_type_id = "onap.policies.native.Apex"
policy_type_version = "1.0.0"
policy_type = PolicyType(type=policy_type_id, version=policy_type_version)
engine_name = "LinkMonitorApexEngine"
engine_version = "0.0.1"
engine_id = "101"
deployment_port = "12345"

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Setup the simulators before the executing the tests."""
    logger.info("Test class setup for Apex tests")
    dmaap_utils.clean_dmaap(settings.DMAAP_GROUP, settings.DMAAP_USER)
    network_simulators.start_and_wait_network_simulators()

    # Wait enough time to have at least the SDNR notifications sent

    logger.info("Waiting 10s that SDNR sends all registration events to VES...")
    time.sleep(10)
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    network_simulators.stop_network_simulators()
    policy.undeploy_policy(policy_id, policy_version, settings.POLICY_BASICAUTH)
    policy.delete_policy(policy_type, policy_id, policy_version, settings.POLICY_BASICAUTH)
    time.sleep(10)
    logger.info("Test Session cleanup done")

def create_policy():
    """Create the policy."""
    logger.info("Create policy")
    policy_data = jinja_env().get_template("ToscaPolicy.json.j2").render(policyId=policy_id, policyVersion=policy_version, policyTypeId=policy_type_id, policyTypeVersion=policy_type_version, engineName=engine_name, engineVersion=engine_version, engineId=engine_id, deploymentPort=deployment_port, dmaapGroup=settings.DMAAP_GROUP, dmaapUser=settings.DMAAP_USER)
    policy.create_policy(policy_type, policy_data, settings.POLICY_BASICAUTH)

    logger.info("Verify whether policy created successfully")
    assert policy.get_policy(policy_type, policy_id, policy_version, settings.POLICY_BASICAUTH).status_code == 200


def deploy_policy():
    """Deploy the policy."""
    logger.info("Deploy policy")
    policy_to_deploy = jinja_env().get_template("DeployPolicyPAP.json.j2").render(policyId=policy_id, policyVersion=policy_version)
    policy.deploy_policy(policy_to_deploy, settings.POLICY_BASICAUTH)
    wait(lambda: check_policy_deployment(), sleep_seconds=10, timeout_seconds=60, waiting_for="Policy Deployment to be OK")

def check_policy_deployment():
    """Verify the policy deployment."""
    logger.info("Verify if the policy is deployed")
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)

    for status in policy_status_list:
        logger.info("the status %s,%s,%s:", status["policy"]["name"], status["policy"]["version"], status["deploy"])
        if (status["policy"]["name"] == policy_id and status["policy"]["version"] == policy_version and status["deploy"] and status["state"] == "SUCCESS"):
            logger.info("Policy deployement OK")
            return True
    logger.info("Policy deployement not yet OK")
    return False

def send_dmaap_event():
    """Send a event to Dmaap that should trigger the apex policy."""
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    dmaap.send_link_failure_event(event)

def test_apex_policy():
    """Test the apex policy."""
    logger.info("Check O-du/O-ru status")
    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"
    send_dmaap_event()
    create_policy()
    deploy_policy()
    time.sleep(10)

    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"
