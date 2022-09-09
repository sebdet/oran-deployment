#!/usr/bin/env python3
###
# ============LICENSE_START===================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
#  Copyright (C) 2022 AT&T Intellectual Property. All rights
#                             reserved.
# ============================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============LICENSE_END=====================================================
#
###
"""Update UUI configuration for Network Slicing option2 test."""
import logging
import logging.config
import subprocess
from subprocess import check_output
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start UUI Preparation")

class UuiPreparation():
    """Can be used to prepare UUI for Network Slicing usecase option2."""

    @classmethod
    def prepare_uui(cls, cst_uuid, cst_invariant_id):
        """Register services to uui."""
        logger.info("####################### Start to update uui settings")
        uui_pod = subprocess.run("kubectl get pod -n onap | grep uui-server | awk '{print $1}' ", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        cmd = f"kubectl exec -ti -n onap {uui_pod} -- sed -i 's/8ee5926d-720b-4bb2-86f9-d20e921c143b/{cst_uuid}/g' /home/uui/config/slicing.properties"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {uui_pod} -- sed -i 's/e75698d9-925a-4cdd-a6c0-edacbe6a0b51/{cst_invariant_id}/g' /home/uui/config/slicing.properties"
        check_output(cmd, shell=True).decode('utf-8')

    @classmethod
    def cleanup_uui(cls, cst_uuid, cst_invariant_id):
        """Rollback uui settings."""
        logger.info("####################### Start to rollback uui settings")
        uui_pod = subprocess.run("kubectl get pod -n onap | grep uui-server | awk '{print $1}' ", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        cmd = f"kubectl exec -ti -n onap {uui_pod} -- sed -i 's/{cst_uuid}/8ee5926d-720b-4bb2-86f9-d20e921c143b/g' /home/uui/config/slicing.properties"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {uui_pod} -- sed -i 's/{cst_invariant_id}/e75698d9-925a-4cdd-a6c0-edacbe6a0b51/g' /home/uui/config/slicing.properties"
        check_output(cmd, shell=True).decode('utf-8')
        logger.info("####################### UUI settings rollback successfully")
