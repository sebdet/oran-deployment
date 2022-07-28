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

"""Smo NonRtric module."""
import logging
import logging.config
from onapsdk.configuration import settings
from waiting import wait
from smo.onap import Onap
from smo.nonrtric import NonRTRic

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Smo k8s")

class Smo():
    """Check SMo nonrtric k8s deployment."""

    onap = Onap()
    non_rt_ric = NonRTRic()

    @classmethod
    def wait_for_smo_to_be_running(cls):
        """Check and wait for the SMo to be running."""
        wait(lambda: cls.onap.is_onap_up() and cls.non_rt_ric.is_nonrtric_up(), sleep_seconds=settings.SMO_CHECK_RETRY, timeout_seconds=settings.SMO_CHECK_TIMEOUT, waiting_for="SMO to be ready")
