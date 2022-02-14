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

"""Onap k8s module."""
import logging

import logging.config

from subprocess import check_output, run
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Onap k8s")

class Onap():
    """Can be used to check onap platform in K8S."""

    @classmethod
    def is_onap_up(cls) -> bool:
        """Verify if ONAP platform is up or not."""
        cmd = "kubectl get pods --field-selector 'status.phase=Failed' -n onap -o name | xargs kubectl delete -n onap"
        run(cmd, shell=True, check=False)
        cmd = "kubectl get pods --field-selector status.phase!=Running -n onap | wc -l"
        result = check_output(cmd, shell=True).decode('utf-8')
        logger.info("Number of Onap pods not in Running state (expected <= %s): %s", settings.ONAP_PODS_WHEN_READY, result)
        if int(result) <= settings.ONAP_PODS_WHEN_READY:
            logger.info("ONAP is Up")
            return True
        logger.info("ONAP is Down")
        return False
