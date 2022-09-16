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
"""Onap MSB module."""
from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.utils.headers_creator import headers_msb_creator

class OranMsb(OnapService):
    """MSB class."""

    base_url = f"{settings.MSB_URL}/api/msdiscover/v1/services"
    headers = headers_msb_creator(OnapService.headers)

    def get_services(self) -> dict:
        """
        Get MSB instance services.

        Returns:
           the list of instance services

        """
        status = self.send_message_json('GET',
                                        'Get status of MSB',
                                        self.base_url,
                                        headers=self.headers)
        return status

    def create_service(self, service_data) -> None:
        """
        Create an instance service.

        Args:
           service_data: the service to be created

        """
        self.send_message('POST', 'Create Instance Service', self.base_url, data=service_data, headers=self.headers)

    def delete_service(self, service_name, version) -> None:
        """
        Delete an instance service.

        Args:
           service_name: the service to be deleted

        """
        url = f"{self.base_url}/{service_name}/version/{version}?namespace="
        self.send_message('DELETE', 'Delete Instance Service', url, headers=self.headers)
