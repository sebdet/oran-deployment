#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import json

BASIC_AUTH = {}

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test O1")

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
