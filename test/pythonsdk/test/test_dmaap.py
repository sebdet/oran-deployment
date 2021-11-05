#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
import logging
from onapsdk.configuration import settings
from oransdk.dmaap.oran_dmaap import OranDmaap
from oransdk.a1sim.a1sim import A1sim

BASIC_AUTH = {}
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

dmaap = OranDmaap()
logger.info("Get all the topics")
topiclist = dmaap.get_all_topics(BASIC_AUTH)
logger.info("response is: %s", topiclist)


logger.info("Create new topic")
topic = '{  "topicName": "unauthenticated.SEC_FAULT_OUTPUT",  "topicDescription": "test topic",  "partitionCount": 1,  "replicationCnCount": 1,  "transactionEnabled": "false"}'
response = dmaap.create_topic(topic, BASIC_AUTH)
logger.info("response is: %s", response)


logger.info("Get topics again")
topiclist = dmaap.get_all_topics(BASIC_AUTH)
logger.info("response is: %s", topiclist)



logger.info("Get ric version for ost")
a1sim = A1sim()
version1 = a1sim.check_version(settings.A1SIM_OST_URL)
version2 = a1sim.check_version(settings.A1SIM_STD1_URL)
version3 = a1sim.check_version(settings.A1SIM_STD2_URL)