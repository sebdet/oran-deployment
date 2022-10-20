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
    def clean_instance(cls, usecase_name):
        """Clean template instance."""
        clamp.change_instance_status("UNINITIALISED", usecase_name, "1.2.3")
        wait(lambda: clamp.verify_instance_status("UNINITIALISED"), sleep_seconds=5, timeout_seconds=300,
             waiting_for="Clamp instance switches to UNINITIALISED")

        logger.info("Delete Instance")
        clamp.delete_template_instance(usecase_name, "1.2.3")
        logger.info("Decommission tosca")
        clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")

    @classmethod
    def create_instance(cls, usecase_name, commissioning_payload, instance_payload) -> bool:
        """Create template instance."""
        response = clamp.upload_commission(commissioning_payload)
        if response["errorDetails"] is not None:
            return False

        logger.info("Create Instance")
        response = clamp.create_instance(instance_payload)
        if response["errorDetails"] is not None:
            return False

        logger.info("Change Instance Status to PASSIVE")
        clamp.change_instance_status("PASSIVE", usecase_name, "1.2.3")
        wait(lambda: clamp.verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=300,
             waiting_for="Clamp instance switches to PASSIVE")

        return True
