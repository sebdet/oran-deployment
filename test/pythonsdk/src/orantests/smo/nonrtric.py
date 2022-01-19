#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
import logging.config
from onapsdk.configuration import settings
from subprocess import check_output

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("NonRTRIc k8s")

class NonRTRic():
    @classmethod
    def is_nonrtric_up(cls):
        cmd="kubectl get pods --field-selector status.phase!=Running -n nonrtric | wc -l"
        result=check_output(cmd, shell=True).decode('utf-8')
        logger.info (f"Number of NonRTRIC pods not in Running state (expected == 0):{result}")
        if int(result) == 0:
            logger.info ("NONRTRIC is Up")
            return True
        else:
            logger.info ("NONRTRIC is Down")
            return False
