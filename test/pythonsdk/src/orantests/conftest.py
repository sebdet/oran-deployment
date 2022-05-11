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
"""Module called by pytest."""
import logging
import logging.config
import os
from requests import RequestException
from onapsdk.configuration import settings
from onapsdk.exceptions import ConnectionFailed, APIError
from waiting import wait
from urllib3.exceptions import NewConnectionError
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.policy.policy import OranPolicy
from oransdk.sdnc.sdnc import OranSdnc
from smo.smo import Smo
from smo.network_simulators import NetworkSimulators

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Session setup")

network_sims = NetworkSimulators("./resources")
smo = Smo()
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)
dmaap = OranDmaap()
sdnc = OranSdnc()
policy = OranPolicy()

def policy_component_ready():
    """Check if components are ready."""
    logger.info("Verify policy components are ready")
    try:
        policy_ready = {"api_ready": False, "pap_ready": False, "apex_ready": False}
    except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
        logger.error(e)
        return False
    policy_status = policy.get_components_status(settings.POLICY_BASICAUTH)
    if (policy_status["api"]["healthy"] and not policy_ready["api_ready"]):
        logger.info("Policy Api is ready")
        policy_ready["api_ready"] = True
    if (policy_status["pap"]["healthy"] and not policy_ready["pap_ready"]):
        logger.info("Policy Pap is ready")
        policy_ready["pap_ready"] = True
    if (len(policy_status["pdps"]["apex"]) > 0 and policy_status["pdps"]["apex"][0]["healthy"] == "HEALTHY" and not policy_ready["apex_ready"]):
        logger.info("Policy Apex is ready")
        policy_ready["apex_ready"] = True
    return policy_ready["api_ready"] and policy_ready["pap_ready"] and policy_ready["apex_ready"]

def sdnc_component_ready():
    """Check if SDNC component is ready."""
    logger.info("Verify sdnc component is ready")

    try:
        response = OranSdnc.get_events(settings.SDNC_BASICAUTH, "test")
    except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
        logger.error(e)
        return False
    return response.status_code == 200

def clamp_component_ready():
    """Check if Clamp component is ready."""
    logger.info("Verify Clamp component is ready")
    try:
        response = clamp.get_template_instance()
    except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
        logger.error(e)
        return False
    return response["automationCompositionList"] is not None

###### Entry points of PYTEST Session
def pytest_sessionstart():
    """Pytest calls it when starting a test session."""
    logger.info("Check and wait for SMO to be running")
    smo.wait_for_smo_to_be_running()
    logger.info("Check and for for SDNC to be running")
    wait(lambda: policy_component_ready(), sleep_seconds=settings.POLICY_CHECK_RETRY, timeout_seconds=settings.POLICY_CHECK_TIMEOUT, waiting_for="Policy to be ready")
    wait(lambda: sdnc_component_ready(), sleep_seconds=settings.SDNC_CHECK_RETRY, timeout_seconds=settings.SDNC_CHECK_TIMEOUT, waiting_for="SDNC to be ready")
    # disable for now, until policy/clamp issue has been fixed
    ##wait(lambda: clamp_component_ready(), sleep_seconds=settings.CLAMP_CHECK_RETRY, timeout_seconds=settings.CLAMP_CHECK_TIMEOUT, waiting_for="Clamp to be ready")

    ## Just kill any simulators that could already be runnin
    network_sims.stop_network_simulators()
    ###### END of FIRST start, now we can start the sims for the real tests.
    logger.info("Tests session setup is ready")
