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
"""Module called by pytest."""
import logging
import logging.config
from onapsdk.configuration import settings
from waiting import wait
from oransdk.utils.healthcheck import HealthCheck

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Session setup")

###### Entry points of PYTEST Session
def pytest_sessionstart():
    """Pytest calls it when starting a test session."""
    logger.info("Check and wait for SMO to be running")
    wait(lambda: HealthCheck.is_onap_up(12), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="SMO to be ready")
    logger.info("Check and wait for for Policy to be running")
    wait(lambda: HealthCheck.policy_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="Policy to be ready")
    logger.info("Check and wait for for SDNC to be running")
    wait(lambda: HealthCheck.sdnc_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="SDNC to be ready")
    logger.info("Check and wait for for SDC to be running")
    wait(lambda: HealthCheck.sdc_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="SDC to be ready")
    logger.info("Check and wait for for AAI to be running")
    wait(lambda: HealthCheck.aai_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="AAI to be ready")
    logger.info("Check and wait for for SO to be running")
    wait(lambda: HealthCheck.so_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="SO to be ready")
    logger.info("Check and wait for for MSB to be running")
    wait(lambda: HealthCheck.msb_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="MSB to be ready")
    logger.info("Check and wait for for OOF to be running")
    wait(lambda: HealthCheck.oof_component_ready(), sleep_seconds=settings.DEFAULT_CHECK_RETRY, timeout_seconds=settings.DEFAULT_CHECK_TIMEOUT, waiting_for="OOF to be ready")


    ###### END of FIRST start, now we can start the sims for the real tests.
    logger.info("Tests session setup is ready")
