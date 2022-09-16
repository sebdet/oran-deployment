#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2022 AT&T Intellectual Property. All rights
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
"""Module called by pytest."""
import logging
import logging.config

from subprocess import check_output, run
from requests import RequestException
from onapsdk.configuration import settings
from onapsdk.exceptions import ConnectionFailed, APIError
from urllib3.exceptions import NewConnectionError
from oransdk.aai.aai import Aai
from oransdk.msb.msb_microservice import OranMsb
from oransdk.oof.oof import Oof
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.policy.policy import OranPolicy
from oransdk.sdc.sdc import SdcTemplate
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.so.so import OranSo

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Health check")

clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)
sdnc = OranSdnc()
policy = OranPolicy()
aai = Aai()
sdc = SdcTemplate()
so = OranSo()
msb = OranMsb()
oof = Oof()

class HealthCheck():
    """Healthcheck class for ONAP component."""

    @classmethod
    def is_onap_up(cls, up_no) -> bool:
        """Verify if ONAP platform is up or not."""
        cmd = "kubectl get pods --field-selector 'status.phase=Failed' -n onap -o name | xargs kubectl delete -n onap"
        run(cmd, shell=True, check=False)
        cmd = "kubectl get pods --field-selector status.phase!=Running -n onap | wc -l"
        result = check_output(cmd, shell=True).decode('utf-8')
        logger.info("Number of Onap pods not in Running state (expected <= %s): %s", up_no, result)
        if int(result) <= up_no:
            logger.info("ONAP is Up")
            return True
        logger.info("ONAP is Down")
        return False

    @classmethod
    def policy_component_ready(cls):
        """Check if Policy components are ready."""
        logger.info("Verify Policy components are ready")
        try:
            policy_ready = {"api_ready": False, "pap_ready": False, "apex_ready": False}
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        policy_status = policy.get_components_status(settings.POLICY_BASICAUTH)
        if (policy_status["api"]["healthy"] and not policy_ready["api_ready"]):
            logger.info("Policy Api is ready")
            policy_ready["api_ready"] = True
        if (policy_status["pap"]["healthy"] and not policy_ready["pap_ready"]):
            logger.info("Policy Pap is ready")
            policy_ready["pap_ready"] = True
        if (len(policy_status["pdps"]["apex"]) > 0 and policy_status["pdps"]["apex"][0]["healthy"] == "HEALTHY" and not policy_ready["apex_ready"]):
            logger.info("Policy Apex is ready")
            policy_ready["apex_ready"] = True
        return policy_ready["api_ready"] and policy_ready["pap_ready"] and policy_ready["apex_ready"]

    @classmethod
    def sdnc_component_ready(cls):
        """Check if SDNC component is ready."""
        logger.info("Verify SDNC component is ready")

        try:
            response = OranSdnc.get_events(settings.SDNC_BASICAUTH, "test")
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response.status_code == 200

    @classmethod
    def clamp_component_ready(cls):
        """Check if Clamp component is ready."""
        logger.info("Verify Clamp component is ready")
        try:
            response = clamp.get_template_instance()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response["automationCompositionList"] is not None

    @classmethod
    def sdc_component_ready(cls):
        """Check if SDC component is ready."""
        logger.info("Verify SDC component is ready")

        try:
            response = sdc.healthcheck()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False

        so_ready = {"BE": False, "CASSANDRA": False, "ON_BOARDING": False, "JANUSGRAPH": False}
        so_list = response["componentsInfo"]
        for so_status in so_list:
            if (so_status["healthCheckComponent"] == "BE" and so_status["healthCheckStatus"] == "UP"):
                so_ready["BE"] = True
            if (so_status["healthCheckComponent"] == "CASSANDRA" and so_status["healthCheckStatus"] == "UP"):
                so_ready["CASSANDRA"] = True
            if (so_status["healthCheckComponent"] == "ON_BOARDING" and so_status["healthCheckStatus"] == "UP"):
                so_ready["ON_BOARDING"] = True
            if (so_status["healthCheckComponent"] == "JANUSGRAPH" and so_status["healthCheckStatus"] == "UP"):
                so_ready["JANUSGRAPH"] = True

        return so_ready["BE"] and so_ready["CASSANDRA"] and so_ready["ON_BOARDING"] and so_ready["JANUSGRAPH"]

    @classmethod
    def aai_component_ready(cls):
        """Check if AAI component is ready."""
        logger.info("Verify AAI component is ready")

        try:
            response = aai.healthcheck()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return "Successful health check:OK" in str(response)

    @classmethod
    def so_component_ready(cls):
        """Check if SO component is ready."""
        logger.info("Verify SO component is ready")

        try:
            response = so.healthcheck()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response["status"] == "UP"

    @classmethod
    def msb_component_ready(cls):
        """Check if MSB component is ready."""
        logger.info("Verify MSB component is ready")

        try:
            response = msb.get_services()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response is not None and len(response) > 0

    @classmethod
    def oof_component_ready(cls):
        """Check if OOF component is ready."""
        logger.info("Verify OOF component is ready")

        try:
            response = oof.get_versions()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response["versions"] is not None
