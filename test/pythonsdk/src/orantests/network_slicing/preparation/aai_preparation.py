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
"""Configure AAI for Network Slicing option2 test."""
import logging
import logging.config

from onapsdk.aai.business.customer import Customer
from onapsdk.configuration import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start AAI Preparation")

class AaiPreparation():
    """Can be used to prepare AAI for Network Slicing usecase option2."""

    @classmethod
    def prepare_aai(cls):
        """Prepare AAI for network slicing use case."""
        logger.info("####################### Start to prepare AAI")
        aai = Customer("5GCustomer", "5GCustomer", "INFRA")
        aai.create("5GCustomer", "5GCustomer", "INFRA")
        aai.subscribe_service("5G")

    @classmethod
    def cleanup_aai(cls):
        """Clean up AAI settings."""
        logger.info("####################### Start to clean up AAI settings")
        aai = Customer.get_by_global_customer_id("5GCustomer")
        aai.delete()
