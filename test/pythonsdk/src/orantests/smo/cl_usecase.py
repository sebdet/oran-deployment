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

"""Cl usecase utils module."""

import logging.config
from waiting import wait
from onapsdk.configuration import settings
from oransdk.policy.clamp import ClampToscaTemplate

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Cl usecae utils")
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)


class ClCommissioningUtils():
    """Can be used to have cl usecase utils methods."""

    @classmethod
    def clean_instance(cls):
        """Clean template instance."""
        clamp.change_instance_status("PASSIVE", "PMSH_Instance1", "1.2.3")
        wait(lambda: clamp.verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60,
             waiting_for="Clamp instance switches to PASSIVE")
        clamp.change_instance_status("UNINITIALISED", "PMSH_Instance1", "1.2.3")
        wait(lambda: clamp.verify_instance_status("UNINITIALISED"), sleep_seconds=5, timeout_seconds=60,
             waiting_for="Clamp instance switches to UNINITIALISED")

        logger.info("Delete Instance")
        clamp.delete_template_instance("PMSH_Instance1", "1.2.3")
        logger.info("Decommission tosca")
        clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")

    @classmethod
    def create_instance(cls, tosca_template) -> bool:
        """Create template instance."""
        response = clamp.upload_commission(tosca_template)
        if response["errorDetails"] is not None:
            return False

        logger.info("Create Instance")
        response = clamp.create_instance(tosca_template)
        if response["errorDetails"] is not None:
            return False

        logger.info("Change Instance Status to PASSIVE")
        clamp.change_instance_status("PASSIVE", "PMSH_Instance1", "1.2.3")
        wait(lambda: clamp.verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60,
             waiting_for="Clamp instance switches to PASSIVE")

        logger.info("Change Instance Status to RUNNING")
        clamp.change_instance_status("RUNNING", "PMSH_Instance1", "1.2.3")
        wait(lambda: clamp.verify_instance_status("RUNNING"), sleep_seconds=5, timeout_seconds=60,
             waiting_for="Clamp instance switches to RUNNING")

        return True
