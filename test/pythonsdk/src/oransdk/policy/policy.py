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
"""Onap Policy module."""

from dataclasses import dataclass
from typing import Dict
from onapsdk.onap_service import OnapService
from oransdk.configuration import settings

@dataclass
class PolicyType:
    """PolicyType dataclass."""

    type: str
    version: str


class OranPolicy(OnapService):
    """Onap Policy library."""

    pap_url = settings.POLICY_PAP_URL
    api_url = settings.POLICY_API_URL
    header = {"Accept": "application/json", "Content-Type": "application/json"}

    @classmethod
    def get_components_status(cls,
                              basic_auth: Dict[str, str]) -> Dict:
        """
        Get status of Policy component.

        Args:
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
           the status of the Policy component

        """
        url = f"{cls.pap_url}/policy/pap/v1/components/healthcheck"
        status = cls.send_message_json('GET',
                                       'Get status of Policy component',
                                       url,
                                       basic_auth=basic_auth)
        return status

    @classmethod
    def get_policy_status(cls, basic_auth: Dict[str, str]) -> Dict:
        """
        Get status of all the policies.

        Returns:
           the status of all the policies

        """
        url = f"{cls.pap_url}/policy/pap/v1/policies/status"
        status = cls.send_message_json('GET',
                                       'Get status of all the policies',
                                       url,
                                       basic_auth=basic_auth)
        return status

    @classmethod
    def get_policy(cls, policy_type: PolicyType, policy_name, policy_version, basic_auth: Dict[str, str]) -> Dict:
        """
        Get the policy.

        Args:
           policy_type: the policy type
           policy_name: the policy name
           policy_version: the version of the policy
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
           the policy reponse

        """
        url = f"{cls.api_url}/policy/api/v1/policytypes/{policy_type.type}/versions/{policy_type.version}/policies/{policy_name}/versions/{policy_version}"
        policy_response = cls.send_message('GET', 'Get the policy', url, basic_auth=basic_auth)
        return policy_response

    @classmethod
    def create_policy(cls, policy_type: PolicyType, policy_data, basic_auth: Dict[str, str]) -> None:
        """
        Create a policy.

        Args:
           policy_type: the policy type
           type_version: the version of the policy type
           policy_data: the policy to be created, in binary format

        """
        url = f"{cls.api_url}/policy/api/v1/policytypes/{policy_type.type}/versions/{policy_type.version}/policies"
        cls.send_message('POST', 'Create Policy', url, data=policy_data, headers=cls.header,
                         basic_auth=basic_auth)

    @classmethod
    def deploy_policy(cls, policy_data, basic_auth: Dict[str, str]) -> None:
        """
        Deploy a policy.

        Args:
           policy_data: the policy to be deployed, in binary format

        """
        url = f"{cls.pap_url}/policy/pap/v1/pdps/policies"
        cls.send_message('POST', 'Deploy Policy', url, data=policy_data, headers=cls.header, basic_auth=basic_auth)

    @classmethod
    def undeploy_policy(cls, policy_id, policy_version, basic_auth: Dict[str, str]) -> None:
        """
        Undeploy a policy.

        Args:
           policy_id: The policy id as provided during the create
           policy_version: The policy version as provided during the create

        """
        url = f"{cls.pap_url}/policy/pap/v1/pdps/policies/{policy_id}/versions/{policy_version}"
        cls.send_message('DELETE', 'Undeploy Policy', url, headers=cls.header, basic_auth=basic_auth)

    @classmethod
    def delete_policy(cls, policy_type: PolicyType, policy_id, policy_version, basic_auth: Dict[str, str]) -> None:
        """
        Delete a policy.

        Args:
           policy_type: the policy type
           policy_id: The policy id as provided during the create
           policy_version: The policy version as provided during the create

        """
        url = f"{cls.api_url}/policy/api/v1/policytypes/{policy_type.type}/versions/{policy_type.version}/policies/{policy_id}/versions/{policy_version}"
        cls.send_message('DELETE', 'Delete Policy', url, headers=cls.header, basic_auth=basic_auth)
