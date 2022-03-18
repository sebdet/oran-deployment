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

"""Dmaap utils module."""
import logging
import logging.config
from onapsdk.configuration import settings
from waiting import wait
from oransdk.dmaap.dmaap import OranDmaap

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("DMaap utils")
dmaap = OranDmaap()

class DmaapUtils():
    """Can be used to have dmaap utils methods."""

    @classmethod
    def clean_dmaap(cls, dmaap_group, dmaap_user):
        """Clean DMAAP useful topics."""
        dmaap.create_topic(settings.DMAAP_TOPIC_FAULT_JSON)
        dmaap.create_topic(settings.DMAAP_TOPIC_PNFREG_JSON)
        # Purge the FAULT TOPIC
        wait(lambda: (dmaap.get_message_from_topic(settings.DMAAP_TOPIC_FAULT, 5000, dmaap_group, dmaap_user).json() == []), sleep_seconds=10, timeout_seconds=60, waiting_for="DMaap topic SEC_FAULT_OUTPUT to be empty")
        wait(lambda: (dmaap.get_message_from_topic(settings.DMAAP_TOPIC_PNFREG, 5000, dmaap_group, dmaap_user).json() == []), sleep_seconds=10, timeout_seconds=60, waiting_for="DMaap topic unauthenticated.VES_PNFREG_OUTPUT to be empty")
