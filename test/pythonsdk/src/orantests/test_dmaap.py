#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
from pathlib import Path
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.a1sim.a1sim import A1sim
from oransdk.utils.jinja import jinja_env

BASIC_AUTH = {}

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test DMAAP")

#dmaap = OranDmaap()
#logger.info("Get all the topics")
#topiclist = dmaap.get_all_topics(BASIC_AUTH)
#logger.info("response is: %s", topiclist)


#logger.info("Create new topic")
#topic = '{  "topicName": "unauthenticated.SEC_FAULT_OUTPUT",  "topicDescription": "test topic",  "partitionCount": 1,  "replicationCnCount": 1,  "transactionEnabled": "false"}'
#response = dmaap.create_topic(topic, BASIC_AUTH)
#logger.info("response is: %s", response)


#logger.info("Get topics again")
#topiclist = dmaap.get_all_topics(BASIC_AUTH)
#logger.info("response is: %s", topiclist)


def test_dmaap():
    logger.info("Get ric version for ost")
    a1sim = A1sim()
    version1 = a1sim.check_version(settings.A1SIM_OSC_URL)

    status = a1sim.check_status(settings.A1SIM_OSC_URL)

    number = a1sim.get_policy_number(settings.A1SIM_OSC_URL)

    data = jinja_env().get_template("OSC/policy_type.json.j2").render()
    a1sim.create_policy_type(settings.A1SIM_OSC_URL, 1, data)
    assert(True)
