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
"""O1 tests module."""
import datetime
import logging
import json
import os
import time
import pytest
from onapsdk.configuration import settings
from smo.network_simulators import NetworkSimulators
from smo.dmaap import DmaapUtils
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.sdnc.sdnc import OranSdnc

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test O1")

network_simulators = NetworkSimulators("./resources")
dmaap = OranDmaap()
dmaap_utils = DmaapUtils()
test_session_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Setup the simulators before the executing the tests."""
    logger.info("Test class setup for O1 tests")

    # Do a first get to register the o1test/o1test user in DMAAP
    # all registration messages will then be stored for the registration tests.
    # If it exists already it clears all cached events.

    dmaap_utils.clean_dmaap(settings.DMAAP_GROUP, settings.DMAAP_USER)

    network_simulators.start_and_wait_network_simulators()
  # ADD DU RESTART just in case
    # Wait enough time to have at least the SDNR notifications sent
    logger.info("Waiting 20s that SDNR sends all registration events to VES...")
    time.sleep(20)
    logger.info("Enabling faults/events reporting on SDNR")
    network_simulators.enable_events_for_all_simulators()
#    logger.info("Waiting 20s that the Dmaap faults topic is created...")
#    time.sleep(20)
    # Preparing the DMaap to cache all the events for the fault topics.
    # If it exists already it clears all cached events.
    logger.info("Waiting 300s to have registration and faults events in DMaap")
    time.sleep(300)
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    network_simulators.stop_network_simulators()
    time.sleep(10)
    logger.info("Test Session cleanup done")

def create_registration_structure(events):
    """Decode the registration events list."""
    devices_found_in_events = dict()
    for event in events:
        event_json = json.loads(event)
        logger.info("Registration json decoded: %s", str(event_json))
        devices_found_in_events[event_json["event"]["commonEventHeader"]["sourceName"]] = event_json["event"]["commonEventHeader"]["reportingEntityName"]

    logger.info("Devices found in events:%s", devices_found_in_events)
    return devices_found_in_events

def create_faults_structure(events):
    """Decode the fault events list."""
    faults_found_in_events = dict()
    for event in events:
        event_json = json.loads(event)
        logger.info("Fault json decoded: %s", str(event_json))
        if event_json["event"]["commonEventHeader"]["sourceName"] in faults_found_in_events:
            faults_found_in_events[event_json["event"]["commonEventHeader"]["sourceName"]] += 1
        else:
            faults_found_in_events[event_json["event"]["commonEventHeader"]["sourceName"]] = 1
    logger.info("Faults found in events: %s", faults_found_in_events)
    return faults_found_in_events

def test_devices_in_sdnc():
    """Verify that the devices are well defined in SDNC."""
    logger.info("Verify if devices are well in SDNC")
    for device in settings.NETWORK_SIMULATORS_LIST:
        logger.info("Verify if %s is well in SDNR", device)
        assert OranSdnc.get_devices(device, settings.SDNC_BASICAUTH) == 200

def validate_faults_timestamp(faults):
    """Extract only the faults returned by SDNC that have been raised during this test."""
    valid_faults = []
    for fault in faults['data-provider:output']['data']:
        try:
            converted_fault_timestamp = datetime.datetime.strptime(fault['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            converted_fault_timestamp = datetime.datetime.strptime(fault['timestamp'], "%Y-%m-%dT%H:%M:%S%z")
        logger.info("Comparing fault timestamp %s (%s) to session test timestamp %s", converted_fault_timestamp, fault['timestamp'], test_session_timestamp)
        if converted_fault_timestamp > test_session_timestamp:
            valid_faults.append(fault)
    logger.info("Valid faults array: %s", valid_faults)
    return valid_faults

def test_device_faults_in_sdnc():
    """Verify that the device faults are well defined in SDNC."""
    logger.info("Verify is there is any events")
    for device in settings.NETWORK_SIMULATORS_DU_RU_LIST:
        faults = OranSdnc.get_events(settings.SDNC_BASICAUTH, device).json()
        logger.info("Verify if %s has events", device)
        assert len(validate_faults_timestamp(faults)) >= 3

def test_network_devices_registration_in_dmaap():
    """Validate that the devices are well registered in SDNR and forwarded to VES."""
    logger.info("Verify if SDNR sends well the RU registration to VES by checking in DMAAP")
    # As the user has been registered in DMAAP during test session init,
    # that call should return all sims registered by SDNR
    all_registrations = []
    events = []

    while (events := dmaap.get_message_from_topic(settings.DMAAP_TOPIC_PNFREG, 30000, settings.DMAAP_GROUP, settings.DMAAP_USER).json()) != []:
        logger.info("Getting a first set of event: %s", events)
        all_registrations += events

    logger.info("ALl registration events received: %s", all_registrations)
    # events should be a list of messages
    logger.info("Verify if the number of events is well >= to the number of expected devices")
    # The DU can send multiple times message to VES and SDNR can send multiple time event for RU
    assert len(all_registrations) >= (len(settings.NETWORK_SIMULATORS_DU_RU_LIST))
    devices_registered = create_registration_structure(all_registrations)

    # Each device must be at least one time in the event list
    for sim_name in settings.NETWORK_SIMULATORS_DU_RU_LIST:
        logger.info("Checking if %s is in events list", sim_name)
        assert sim_name in devices_registered
        if "o-ru" in sim_name:
            logger.info("RU event detected checking SDNR has well registered it")
            assert "ONAP SDN-R" in devices_registered[sim_name]
        elif "o-du" in sim_name:
            logger.info("DU detected checking it has well registered itself")
            assert "o-du" in devices_registered[sim_name]

def test_device_faults_in_dmaap():
    """Verify that device faults are well sent to DMAAP by SDNR."""
    logger.info("Verify if SDNR forwards well the faults sent by the simulators to DMAAP")
    events = dmaap.get_message_from_topic(settings.DMAAP_TOPIC_FAULT, 30000, settings.DMAAP_GROUP, settings.DMAAP_USER).json()
    logger.info("Verify if faults have well been received for each device")
    assert len(events) > 0
    faults_received = create_faults_structure(events)

    # Each device must have some faults
    for sim_name in settings.NETWORK_SIMULATORS_DU_RU_LIST:
        logger.info("Check if %s has at least >=3 faults", sim_name)
        assert sim_name in faults_received and faults_received[sim_name] >= 3
