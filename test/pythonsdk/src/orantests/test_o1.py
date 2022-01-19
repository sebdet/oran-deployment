#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import json
import pytest
from smo.network_simulators import NetworkSimulators
import os

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test O1")

network_simulators = NetworkSimulators("./resources")

@pytest.fixture(scope="class", autouse=True)
def setup_simulators():
    logger.info ("Test class setup for O1 tests")
    network_simulators.start_network_simulators()
    network_simulators.wait_for_network_simulators_to_be_running()
    # Wait enough time to have at least the SDNR notifications sent
    logger.info ("Waiting 60s that SDNR sends all registration events to VES...")
    time.sleep(60)
    logger.info ("Enabling faults/events reporting on SDNR")
    network_simulators.enable_events_for_all_simulators()
    ## Preparing the DMaap to cache all the events for specific topics
    dmaap.get_message_from_topic("unauthenticated.SEC_FAULT_OUTPUT", 1000, settings.DMAAP_GROUP, settings.DMAAP_USER)
    logger.info ("Test Session setup completed successfully")

    ### Cleanup code
    yield
    network_simulators.stop_network_simulators()
    logger.info ("Test Session cleanup done")

def test_network_devices_registration():
    logger.info("Verify if SDNR sends well the RU registration to VES by checking in DMAAP")
    dmaap = OranDmaap()
    # As the user has been registered in DMAAP during test session init, that call should return all sims registered by SDNR
    events = dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 10000, settings.DMAAP_GROUP, settings.DMAAP_USER).json()
    # events should be a list of messages
    logger.info("Verify if the number of events is well equals to the number of devices")
    assert (len(events) >= 6)

    for event in events:
        logger.info(f"Checking event: {event}")
        eventjson = json.loads(event)
        logger.info("json ?"+str(eventjson))
        assert(eventjson["event"]["commonEventHeader"]["sourceName"] in settings.NETWORK_SIMULATOR_DEVICES_LIST)

        if "o-ru" in eventjson["event"]["commonEventHeader"]["sourceName"]:
            logger.info(f"RU event detected checking SDNR has well registered it")
            assert(eventjson["event"]["commonEventHeader"]["reportingEntityName"] == "ONAP SDN-R")
        elif "o-du" in eventjson["event"]["commonEventHeader"]["sourceName"]:
            logger.info(f"DU detected checking it has well registered itself")
            assert("o-du" in eventjson["event"]["commonEventHeader"]["reportingEntityName"])
