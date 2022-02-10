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
"""Onap Clamp module."""

from oransdk.configuration import settings
from onapsdk.clamp.clamp_element import Clamp


class OranClamp(Clamp):
    """SDNC Library."""

    base_url = settings.CLAMP_URL
    header = {"accept": "application/json", "Content-Type": "application/json"}

    @classmethod
    def upload_commission(cls, basic_auth):
        """
        Upload commission
        :param basic_auth:
        :return:
        """
        url = f"{cls.base_url}/clamp/restservices/clds/v2/toscaControlLoop/commissionToscaTemplate"
        return cls.send_message('POST', 'Upload commission', url, basic_auth=basic_auth)

    @classmethod
    def create_instance(cls, clamp_data, basic_auth: [str, str]) -> None :
        """
          Create instance
          :param basic_auth
          Args:
              clamp_data : the clamp to be created in binary format
        """
        url =f"{cls.base_url}/restservices/clds/v2/toscaControlLoop/postToscaInstanceProperties"
        cls.send_message('POST', 'Create Instance', url, data=clamp_data, headers=cls.header, basic_auth=basic_auth)


    @classmethod
    def change_instance_status(cls, clamp_data):
        """
          Change instance
          :param cls:
          :param clamp_data
        """
        url = f"{cls.base_url}/restservices/clds/v2/toscaControlLoop/putToscaInstantiationStateChange"
        cls.send_message('PUT', 'Change instance', url, data=clamp_data, headers=cls.header)

    @classmethod
    def delete_instance(cls):
        """
        Delete instance
        :return:
        """
        url = f"{cls.base_url}/restservices/clds/v2/toscaControlLoop/deleteToscaInstanceProperties?name=PMSH_Instance1&version=1.2.3"
        cls.send_message('DELETE', 'Delete instance', url, headers=cls.header)

    @classmethod
    def decommission_template(cls):
        """
        Decommision template
        :return:
        """
        url = f"{cls.base_url}/restservices/clds/v2/toscaControlLoop/decommissionToscaTemplate?name=ToscaServiceTemplateSimple&version=1.0.0"
        cls.send_message('DELETE', 'Decommision template', url, headers=cls.header)
