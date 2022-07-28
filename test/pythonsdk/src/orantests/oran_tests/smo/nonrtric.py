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
