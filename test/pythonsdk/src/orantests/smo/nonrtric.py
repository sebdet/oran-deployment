#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""NonrtRic module."""
import logging
import logging.config
from subprocess import check_output
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("NonRTRIc k8s")

class NonRTRic():
    """Control the Nonrtric k8s deployment."""

    @classmethod
    def is_nonrtric_up(cls):
        """Check if the nonrtric is up."""
        cmd = "kubectl get pods --field-selector status.phase!=Running -n nonrtric | wc -l"
        result = check_output(cmd, shell=True).decode('utf-8')
        logger.info("Number of NonRTRIC pods not in Running state (expected == 0):%s", result)
        if int(result) == 0:
            logger.info("NONRTRIC is Up")
            return True

        logger.info("NONRTRIC is Down")
        return False
