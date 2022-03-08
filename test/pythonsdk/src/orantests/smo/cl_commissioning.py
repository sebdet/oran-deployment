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

"""ClCommisionning module."""
import time
import logging
import logging.config
from requests import RequestException
from onapsdk.configuration import settings
from onapsdk.exceptions import ConnectionFailed, APIError, RequestError
from urllib3.exceptions import NewConnectionError
from oransdk.policy.clamp import ClampToscaTemplate

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("CL Commissioning")
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)

class ClCommissioning():
    """Defines Closed Loop Commisionning related method."""

    @classmethod
    def clamp_component_ready(cls):
        """Check if Clamp component is ready."""
        logger.info("Verify clamp component is ready")

        try:
            response = clamp.get_template_instance()
        except (RequestException, NewConnectionError, ConnectionFailed, APIError) as e:
            logger.error(e)
            return False
        return response["controlLoopList"] is not None

    @classmethod
    def upload_commission(cls, tosca_template):
        """
        Upload the tosca to commissioning.

        Args:
            tosca_template : the tosca template to upload in json format
        Returns:
            the response from the upload action
        """
        logger.info("Upload tosca to commissioning")
        return clamp.upload_commission(tosca_template)

    @classmethod
    def create_instance(cls, tosca_template):
        """
        Create a instance.

            Args:
                tosca_template : the tosca template to create in json format
            Returns:
                the response from the creation action
        """
        logger.info("Create Instance")
        return clamp.create_instance(tosca_template)

    @classmethod
    def change_instance_status(cls, new_status) -> str:
        """
        Change the instance statue.

        Args:
            new_status : the new instance to be changed to
        Returns:
            the new status to be changed to
        """
        logger.info("Change Instance Status to %s", new_status)
        try:
            clamp.change_instance_status(new_status, "PMSH_Instance1", "1.2.3")
        except RequestError:
            logger.info("Change Instance Status request returned failed. Will query the instance status to double check whether the request is successful or not.")

        # There's a bug in Clamp code, sometimes it returned 500, but actually the status has been changed successfully
        # Thus we verify the status to determine whether it was successful or not
        time.sleep(2)
        response = clamp.get_template_instance()
        return response["controlLoopList"][0]["orderedState"]

    @classmethod
    def verify_instance_status(cls, new_status):
        """
        Verify whether the instance changed to the new status.

        Args:
            new_status : the new status of the instance
        Returns:
            the boolean value indicating whether status changed successfully
        """
        logger.info("Verify the Instance Status is updated to the expected status %s", new_status)
        response = clamp.get_template_instance()
        if response["controlLoopList"][0]["state"] == new_status:
            return True
        return False

    @classmethod
    def delete_template_instance(cls):
        """
        Delete the template instance.

        Returns:
            the response from the deletion action
        """
        logger.info("Delete Instance")
        return clamp.delete_template_instance("PMSH_Instance1", "1.2.3")

    @classmethod
    def decommission_tosca(cls):
        """
        Decommission the tosca template.

        Returns:
            the response from the decommission action
        """
        logger.info("Decommission tosca")
        return clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")
