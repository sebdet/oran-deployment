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
"""Network Slicing option2 test module."""

import logging
import logging.config
import pytest
from onapsdk.configuration import settings
from preparation.sdc_preparation import SdcPreparation

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Network Slicing usecase Option2")
sdcPreparation = SdcPreparation()

@pytest.fixture(scope="module", autouse=True)
def pre_config():
    """Set the onap components before executing the tests."""
    logger.info("Test class setup for Network Slicing usecase Option2")

    logger.info("PreConfig Step1: Create SDC Templates")
    sdcPreparation.prepare_sdc()
    logger.info("SDC Templates created successfully")

    ### Cleanup code
    yield
    logger.info("Test Session cleanup done")

def test_network_slicing_option2():
    """The Network Slicing option2 usecase."""
    logger.info("Good")
