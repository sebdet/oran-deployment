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
from onapsdk.configuration import settings
from waiting import wait
from smo.smo import Smo
from smo.network_simulators import NetworkSimulators
from oransdk.utils.healthcheck import HealthCheck


# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Session setup")

network_sims = NetworkSimulators("./resources")
smo = Smo()

###### Entry points of PYTEST Session
def pytest_sessionstart():
    """Pytest calls it when starting a test session."""
    logger.info("Check and wait for SMO to be running")
    smo.wait_for_smo_to_be_running(settings.ONAP_PODS_WHEN_READY)
    logger.info("Check and for for SDNC to be running")
    wait(lambda: HealthCheck.policy_component_ready(), sleep_seconds=settings.POLICY_CHECK_RETRY, timeout_seconds=settings.POLICY_CHECK_TIMEOUT, waiting_for="Policy to be ready")
    wait(lambda: HealthCheck.sdnc_component_ready(), sleep_seconds=settings.SDNC_CHECK_RETRY, timeout_seconds=settings.SDNC_CHECK_TIMEOUT, waiting_for="SDNC to be ready")
    wait(lambda: HealthCheck.clamp_component_ready(), sleep_seconds=settings.CLAMP_CHECK_RETRY, timeout_seconds=settings.CLAMP_CHECK_TIMEOUT, waiting_for="Clamp to be ready")

    ## Just kill any simulators that could already be runnin
    network_sims.stop_network_simulators()
    ###### END of FIRST start, now we can start the sims for the real tests.
    logger.info("Tests session setup is ready")
