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
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.sdnc.sdnc import OranSdnc
from onapsdk.configuration import settings
from waiting import wait
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
dmaap = OranDmaap()
sdnc = OranSdnc()

TOPIC_PNFREG = '{"topicName": "unauthenticated.VES_PNFREG_OUTPUT"}'

TOPIC_FAULT = '{"topicName": "unauthenticated.SEC_FAULT_OUTPUT"}'

#TOPIC_PNFREG = {
#    "owner": "",
#    "readerAcl": {
#        "enabled": "true",
#        "users": []
#    },
#    "name": "unauthenticated.VES_PNFREG_OUTPUT",
#    "description": "",
#    "writerAcl": {
#        "enabled": "true",
#        "users": []
#    }
#}

#TOPIC_FAULT = {
#    "owner": "",
#    "readerAcl": {
#        "enabled": "true",
#        "users": []
#    },
#    "name": "unauthenticated.SEC_FAULT_OUTPUT",
#    "description": "",
#    "writerAcl": {
#        "enabled": "true",
#        "users": []
#    }
#}

###### Entry points of PYTEST Session
def pytest_sessionstart():
    """Pytest calls it when starting a test session."""
    logger.info("Check and wait for SMO to be running")
    smo.wait_for_smo_to_be_running()
    logger.info("Check and for for SDNC to be running")
    wait(lambda: OranSdnc.get_events(settings.SDNC_BASICAUTH, "test").status_code == 200, sleep_seconds=10, timeout_seconds=300, waiting_for="SDNC to be ready")

    dmaap.create_topic(TOPIC_PNFREG)
    dmaap.create_topic(TOPIC_FAULT)
    ### Due to an Onap Ves/dmaap behavior !!! DU sims must send messages
    ### twice so we need to create/delete the sims
#    network_sims.start_network_simulators()
#    network_sims.wait_for_network_simulators_to_be_running()
#    time.sleep(20)
    ## Now kill the simulators and restart them for the test session
    network_sims.stop_network_simulators()
    ###### END of FIRST start, now we can start the sims for the real tests.
