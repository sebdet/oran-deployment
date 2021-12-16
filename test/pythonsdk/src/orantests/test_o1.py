#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import time

BASIC_AUTH = {}

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test O1")

def test_ru_registration():
	logger.info("Verify if SDNR sends well the RU registration to VES by checking in DMAAP")
	dmaap = OranDmaap()
	# As the user has been registered in DMAAP during test session init, that call should return all sims registered by SDNR
	events = dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 10000, settings.DMAAP_GROUP, settings.DMAAP_USER).json()
	#logger.info(f"Json received from DMAAP:{events}")
	assert (len(events) == 6)
