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
from preparation.aai_preparation import AaiPreparation
from preparation.oof_preparation import OofPreparation
from preparation.sdc_preparation import SdcPreparation
from preparation.so_preparation import SoPreparation
from preparation.msb_preparation import MsbPreparation
from preparation.uui_preparation import UuiPreparation

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Network Slicing usecase Option2")
sdc_template_suffix = ""
sdcPreparation = SdcPreparation(sdc_template_suffix)
soPreparation = SoPreparation()
aaiPreparation = AaiPreparation()
oofPreparation = OofPreparation()
msbPreparation = MsbPreparation()
uuiPreparation = UuiPreparation()

@pytest.fixture(scope="module", autouse=True)
def pre_config():
    """Set the onap components before executing the tests."""
    logger.info("Test class setup for Network Slicing usecase Option2")

    logger.info("PreConfig Step1: Create SDC Templates")
    res = sdcPreparation.prepare_sdc()
    cst_id = res[0]
    cst_invariant_id = res[1]
    sp_id = res[2]
    logger.info("SDC Templates created successfully, cst_id:" + cst_id + "; sp_id:" + sp_id + "; cst_invariant_id:" + cst_invariant_id)

    logger.info("PreConfig Step2: AAI Configuration")
    aaiPreparation.prepare_aai()
    logger.info("AAI Configured successfully")

    #cst_id = "test"
    #cst_invariant_id = "test"
    #sp_id = "03d396bf-0246-4d48-817a-b219cc2e7a5a"
    logger.info("PreConfig Step3: SO Configuration")
    soPreparation.prepare_so(cst_id, sp_id)
    logger.info("SO Configured successfully")

    logger.info("PreConfig Step4: OOF Configuration - Optimization Policy Creation")
    oofPreparation.prepare_oof(sdcPreparation.updated_name("EmbbNst_O2"), sdcPreparation.updated_name("EmbbAn_NF"), sdcPreparation.updated_name("Tn_ONAP_internal_BH"))
    logger.info("OOF Configured successfully")

    logger.info("PreConfig Step5: MSB Configuration - Create msb services")
    msbPreparation.prepare_msb()
    logger.info("MSB Configured successfully")

    logger.info("PreConfig Step6: UUI Configuration - Update uui settings")
    uuiPreparation.prepare_uui(cst_id, cst_invariant_id)
    logger.info("UUI Configured successfully")

    ### Cleanup code
    yield
    logger.info("Start to cleanup user case specific configurations")
    #aaiPreparation.cleanup_aai()
    #soPreparation.cleanup_so()
    #oofPreparation.cleanup_oof()
    #msbPreparation.cleanup_msb()
    #uuiPreparation.cleanup_uui(cst_id, cst_invariant_id)
    logger.info("Test Session cleanup done")

def test_network_slicing_option2():
    """The Network Slicing option2 usecase."""
    logger.info("Good")
