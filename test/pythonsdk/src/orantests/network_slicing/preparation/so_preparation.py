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
"""Prepare SO for Network Slicing option2 test."""
import logging
import logging.config
import os
import subprocess
from subprocess import check_output
from onapsdk.configuration import settings

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start SO Preparation")

class SoPreparation():
    """Can be used to prepare SO for Network Slicing usecase option2."""

    @classmethod
    def prepare_so(cls, cst_id, sp_id):
        """Update So catalog db.

        Args:
            cst_id (str): The CST uuid of from the SDC Template creation step.
            sp_id (str): The ServiceProfile uuid from the SDC Template creation step.
        """
        logger.info("####################### Start to update SO catalog DB")
        cmd = "kubectl get secret/onap-mariadb-galera-db-root-password -n onap -o jsonpath={.data.password} | base64 --decode"
        pw = check_output(cmd, shell=True).decode('utf-8')
        #logger.info("####################### pass is:%s", pw)

        # populate communication service actions
        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('createInstance', '1', 'Custom recipe to create communication service-instance if no custom BPMN flow is found', \
              '/mso/async/services/CreateCommunicationService', NULL, 180, NULL, '{cst_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('deleteInstance', '1', 'Custom recipe to delete communication service if no custom BPMN flow is found', \
              '/mso/async/services/DeleteCommunicationService', NULL, 180, NULL, '{cst_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('activateInstance', '1.0', 'activate communication service', '/mso/async/services/ActivateCommunicationService', \
              NULL, 180, NULL, '{cst_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        # populate slice service actions
        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('createInstance', '1', 'Custom recipe to create slice service-instance if no custom BPMN flow is found', \
              '/mso/async/services/CreateSliceService', NULL, 180, NULL, '{sp_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('deleteInstance', '1', 'Custom recipe to create slice service-instance if no custom BPMN flow is found', \
              '/mso/async/services/DeleteSliceService', NULL, 180, NULL, '{sp_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        sql = f"INSERT INTO  \
              catalogdb.service_recipe(ACTION, VERSION_STR, DESCRIPTION, ORCHESTRATION_URI, SERVICE_PARAM_XSD, \
              RECIPE_TIMEOUT, SERVICE_TIMEOUT_INTERIM, SERVICE_MODEL_UUID) \
              VALUES ('activateInstance', '1.0', 'Gr api recipe to activate service-instance', \
              '/mso/async/services/ActivateSliceService', NULL, 180, NULL, '{sp_id}');"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        logger.info("####################### Start to copy subnetCapability.json to SO main pod")
        so_pod = subprocess.run("kubectl get pods -n onap | awk '{print $1}' | grep  onap-so-[a-z0-9]*-[a-z0-9]*$", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        cmd = f"kubectl cp ../resources/subnetCapability.json -n onap {so_pod}:/app"
        check_output(cmd, shell=True).decode('utf-8')

    @classmethod
    def cleanup_so(cls, cst_id, sp_id):
        """Clean up So configuration.

        Args:
            cst_id (str): The CST uuid of from the SDC Template creation step.
            sp_id (str): The ServiceProfile uuid from the SDC Template creation step.
        """
        logger.info("####################### Start to clean up SO catalog DB")
        cmd = "kubectl get secret/onap-mariadb-galera-db-root-password -n onap -o jsonpath={.data.password} | base64 --decode"
        pw = check_output(cmd, shell=True).decode('utf-8')

        # remove communication service actions
        sql = f"Delete from  service_recipe where SERVICE_MODEL_UUID=\"{cst_id}\";"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        # remove slice service actions
        sql = f"Delete from  service_recipe where SERVICE_MODEL_UUID=\"{sp_id}\";"
        cmd = f"kubectl -n onap exec onap-mariadb-galera-0 -- mysql -uroot -p{pw} -D catalogdb -e \"{sql}\""
        check_output(cmd, shell=True).decode('utf-8')

        logger.info("####################### Start to remove subnetCapability.json to SO main pod")
        so_pod = subprocess.run("kubectl get pods -n onap | awk '{print $1}' | grep  onap-so-[a-z0-9]*-[a-z0-9]*$", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        cmd = f"kubectl -n onap exec {so_pod} -- rm -f /app/subnetCapability.json -n onap"
        check_output(cmd, shell=True).decode('utf-8')
