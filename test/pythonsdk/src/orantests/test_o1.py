#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import json
import pytest
from smo.network_simulators import NetworkSimulators
import os
import time

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test O1")

network_simulators = NetworkSimulators("./resources")
dmaap = OranDmaap()

@pytest.fixture(scope="class", autouse=True)
def setup_simulators():
    logger.info ("Test class setup for O1 tests")

    # Do a first get to register the o1test/o1test user in DMAAP,
    # all registration messages will then be stored for the registration tests.
    dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 500, settings.DMAAP_GROUP, settings.DMAAP_USER)

    network_simulators.start_network_simulators()
    network_simulators.wait_for_network_simulators_to_be_running()
    # Wait enough time to have at least the SDNR notifications sent
    logger.info ("Waiting 60s that SDNR sends all registration events to VES...")
    time.sleep(60)
    logger.info ("Enabling faults/events reporting on SDNR")
    network_simulators.enable_events_for_all_simulators()

    ## Preparing the DMaap to cache all the events for the fault topics
    dmaap.get_message_from_topic("unauthenticated.SEC_FAULT_OUTPUT", 500, settings.DMAAP_GROUP, settings.DMAAP_USER)

    logger.info ("Test Session setup completed successfully")

    ### Cleanup code
    yield
    network_simulators.stop_network_simulators()
    logger.info ("Test Session cleanup done")

def decode_registration_events(events):
    devices_found_in_events = dict()
    for event in events:
        event_json = json.loads(event)
        logger.info("json decoded:"+str(event_json))
        devices_found_in_events[event_json["event"]["commonEventHeader"]["sourceName"]] = event_json["event"]["commonEventHeader"]["reportingEntityName"]
    
    logger.info(f"devices_found_in_events:{devices_found_in_events}")
    return devices_found_in_events

def test_network_devices_registration():
    logger.info("Verify if SDNR sends well the RU registration to VES by checking in DMAAP")
    # As the user has been registered in DMAAP during test session init, that call should return all sims registered by SDNR
    events = dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 5000, settings.DMAAP_GROUP, settings.DMAAP_USER).json()
    # events should be a list of messages
    logger.info("Verify if the number of events is well >= to the number of expected devices")
    # The DU can send multiple times message to VES and SDNR can send multiple time event for RU
    assert (len(events) >= (len(settings.NETWORK_SIMULATORS_DU_RU_LIST)+len(settings.NETWORK_SIMULATORS_DU_LIST)))
    devices_registered = decode_registration_events(events)

    # Each device must be at least one time in the event list
    for sim_name in settings.NETWORK_SIMULATORS_DU_RU_LIST:
        logger.info(f"Checking if {sim_name} is in events list")
        sim_found = False
        assert(sim_name in devices_registered)
        if "o-ru" in sim_name:
            logger.info(f"RU event detected checking SDNR has well registered it")
            assert("ONAP SDN-R" in devices_registered[sim_name])
        elif "o-du" in sim_name:
            logger.info(f"DU detected checking it has well registered itself")
            assert("o-du" in devices_registered[sim_name])
