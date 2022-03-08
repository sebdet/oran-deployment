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
"""Onap Sdnc module."""

from typing import Dict
from onapsdk.sdnc.sdnc_element import SdncElement
from oransdk.configuration import settings

class OranSdnc(SdncElement):
    """SDNC library."""

    base_url = settings.SDNC_URL
    header = {"Accept": "application/json", "Content-Type": "application/json"}

    @classmethod
    def get_status(cls) -> str:
        """
        Get status of SDNC component.

        Returns:
           the status of the SDNC component

        """
        url = f"{cls.base_url}/apidoc/explorer/"
        status = cls.send_message('GET',
                                  'Get status of SDNC component',
                                  url)
        return status

    @classmethod
    def get_odu_oru_status(cls,
                           odu_node,
                           radio_unit,
                           basic_auth: Dict[str, str]) -> dict:
        """
        Get status of SDNC component.

        Args:
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
           the status of the SDNC component

        """
        url = f"{cls.base_url}/rests/data/network-topology:network-topology/topology=topology-netconf/node={odu_node}/yang-ext:mount/o-ran-sc-du-hello-world:network-function/distributed-unit-functions={odu_node}/radio-resource-management-policy-ratio={radio_unit}"
        status = cls.send_message_json('GET',
                                       'Get status of Odu connectivity',
                                       url,
                                       basic_auth=basic_auth)
        return status

    @classmethod
    def get_devices(cls, device_node, basic_auth: Dict[str, str]) -> int:
        """
        Get Devices on SDNC.

        Returns:
           the status of the sdnc component
        """
        url = f"{cls.base_url}/rests/data/network-topology:network-topology/topology=topology-netconf/node={device_node}"
        status = cls.send_message('GET', 'Get status of Device connectivity', url, basic_auth=basic_auth)
        return status.status_code

    @classmethod
    def get_events(cls, basic_auth: Dict[str, str], device):
        """
        Create device events in Sdnc.

        Args:
           topic: the event to create, in json format
           :param basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }
           :param device:

        """
        url = f"{cls.base_url}/rests/operations/data-provider:read-faultlog-list"
        return cls.send_message('POST', 'Get SDNC events', url, data='{"input": {"filter": [ {"property": "node-id", "filtervalue": "' + device + '"}],"sortorder":[{"property": "timestamp","sortorder": "descending"}],"pagination": {"size": 10,"page": 1}}}', headers=cls.header, basic_auth=basic_auth)
