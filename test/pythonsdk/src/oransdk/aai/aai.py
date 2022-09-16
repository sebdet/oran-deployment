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
"""Onap AAI module."""
from onapsdk.aai.aai_element import AaiElement
from onapsdk.configuration import settings

class Aai(AaiElement):
    """AAI healthcheck class."""

    def healthcheck(self) -> str:
        """AAI Model healthcheck.

        Returns:
           result of the health check
        """
        res = self.send_message_json("GET", "A&AI healthcheck", f"{self.url}/echo?action=long")
        return res

    @property
    def url(self) -> str:
        """Define the base url.

        Returns:
            the base url of the class

        """
        return f"{settings.AAI_URL}/aai/util"
