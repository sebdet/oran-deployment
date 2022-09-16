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
"""Onap OOF module."""
from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService

class Oof(OnapService):
    """OOF class."""

    def get_versions(self) -> dict:
        """
        Get OOF HAS API supported versions.

        Returns:
           the list of supported versions

        """
        response = self.send_message_json('GET', 'Get OOF supported version', settings.OOF_URL)
        return response
