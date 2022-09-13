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
"""Create MSB Templates for Network Slicing option2 test."""
import logging
import logging.config
import subprocess
from subprocess import check_output
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start MSB Preparation")

class MsbPreparation():
    """Can be used to prepare MSB for Network Slicing usecase option2."""

    @classmethod
    def prepare_msb(cls):
        """Register services to msb."""
        logger.info("####################### Start to register SO instance service")
        so_pod = subprocess.run("kubectl get svc -n onap so | grep so | awk '{print $3}' ", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        content = "{ \"url\": \"/onap/so/infra/e2eServiceInstances/v3\",\"nodes\": [{\"nodeId\": \"_v3_so-serviceInstances_" + so_pod + "_8080\", \
                  \"checkUrl\": \"\",\"status\": \"passing\",\"ha_role\": \"\",\"checkType\": \"\",\"ip\": \""+ so_pod +"\",\"port\": \"8080\", \
                  \"tls_skip_verify\": true}],\"status\": \"1\",\"publish_port\": \"\",\"lb_policy\": \"ip_hash\",\"serviceName\": \
                  \"so-serviceInstances\",\"metadata\": [],\"network_plane_type\": \"\", \"version\": \"v3\",\"labels\": [],\"namespace\": \"\", \
                  \"enable_ssl\": false,\"path\": \"\",\"protocol\": \"REST\",\"host\": \"\",\"visualRange\": \"1\",\"is_manual\": true}"
        cmd = f"curl -sk --noproxy \"*\" -X POST {settings.MSB_URL}/api/msdiscover/v1/services -H  \"accept: application/json\" -H  \"Content-Type: application/json\" -d '{content}'"
        check_output(cmd, shell=True).decode('utf-8')

        logger.info("####################### Start to register SO orchestration tasks")
        content = "{ \"url\": \"/onap/so/infra/orchestrationTasks/v4\",\"nodes\": [{\"nodeId\": \"_v4_so-orchestrationTasks_" + so_pod + "_8080\", \
                  \"checkUrl\": \"\",\"status\": \"passing\",\"ha_role\": \"\",\"checkType\": \"\",\"ip\": \""+ so_pod +"\",\"port\": \"8080\", \
                  \"tls_skip_verify\": true}],\"status\": \"1\",\"publish_port\": \"\",\"lb_policy\": \"ip_hash\",\"serviceName\": \
                  \"so-orchestrationTasks\",\"metadata\": [],\"network_plane_type\": \"\", \"version\": \"v4\",\"labels\": [],\"namespace\": \"\", \
                  \"enable_ssl\": false,\"path\": \"\",\"protocol\": \"REST\",\"host\": \"\",\"visualRange\": \"1\",\"is_manual\": true}"
        cmd = f"curl -sk --noproxy \"*\" -X POST {settings.MSB_URL}/api/msdiscover/v1/services -H  \"accept: application/json\" -H  \"Content-Type: application/json\" -d '{content}'"
        check_output(cmd, shell=True).decode('utf-8')

        logger.info("####################### Start to register AAI business instance service")
        aai_pod = subprocess.run("kubectl get svc -n onap aai | grep aai | awk '{print $3}' ", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        content = '{"url": "/aai/v13/business", "nodes": [{"nodeId": "_v13_aai-business_' + aai_pod + '_8443", \
                  "checkUrl": "","status": "passing","ha_role": "","checkType": "","ip": "' + aai_pod + '", "port": "8443", \
                  "tls_skip_verify": true}],"status": "1","publish_port": "","lb_policy": "", "serviceName": "aai-business","metadata": \
                  [],"network_plane_type": "","version": "v13","labels": [],"namespace": "","enable_ssl": true,"path": "","protocol": \
                  "REST","host": "","visualRange": "1","is_manual": true}'
        cmd = f"curl -sk --noproxy \"*\" -X POST {settings.MSB_URL}/api/msdiscover/v1/services -H  \"accept: application/json\" -H  \"Content-Type: application/json\" -d '{content}'"
        check_output(cmd, shell=True).decode('utf-8')

    @classmethod
    def cleanup_msb(cls):
        """Rollback msb settings."""
        logger.info("####################### Start to remove SO instance service")
        cmd = f"curl -sk --noproxy \"*\" -X DELETE {settings.MSB_URL}/api/msdiscover/v1/services -H  \"accept: application/json\" -H  \"Content-Type: application/json\" "
        check_output(cmd, shell=True).decode('utf-8')
