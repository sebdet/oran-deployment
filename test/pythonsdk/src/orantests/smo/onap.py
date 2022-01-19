#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
import logging.config
from onapsdk.configuration import settings
from subprocess import check_output

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Onap k8s")

class Onap():
   @classmethod
   def is_onap_up(cls):
        cmd="kubectl get pods --field-selector status.phase!=Running -n onap | wc -l"
        result=check_output(cmd, shell=True).decode('utf-8')
        logger.info (f"Number of Onap pods not in Running state (expected <=9): {result}")
        if int(result) <= 9:
            logger.info ("ONAP is Up")
            return True
        else:
            logger.info ("ONAP is Down")
            return False
