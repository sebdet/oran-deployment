#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

"""Onap k8s module."""
import logging

import logging.config

from subprocess import check_output,run
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Onap k8s")

class Onap():
    """Can be used to check onap platform in K8S."""

    @classmethod
    def is_onap_up(cls) -> bool:
        """Verify if ONAP platform is up or not."""
        cmd = "kubectl get pods --field-selector 'status.phase=Failed' -n onap -o name | xargs kubectl delete -n onap"
        run(cmd, shell=True)
        cmd = "kubectl get pods --field-selector status.phase!=Running -n onap | wc -l"
        result = check_output(cmd, shell=True).decode('utf-8')
        logger.info("Number of Onap pods not in Running state (expected <= 8): %s", result)
        if int(result) <= 8:
            logger.info("ONAP is Up")
            return True
        logger.info("ONAP is Down")
        return False
