#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Onap Policy module."""

from dataclasses import dataclass
from typing import Dict
from oransdk.configuration import settings
from onapsdk.onap_service import OnapService

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
    def get_policy_status(cls,
                          basic_auth: Dict[str, str]) -> Dict:
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
    def get_policy(cls,
                   policy_type: PolicyType,
                   policy_name,
                   policy_version,
                   basic_auth: Dict[str, str]) -> Dict:
        """
        Get the policy.

        Args:
           policy_type: the policy type
           policy_name: the policy name
           policy_version: the version of the policy
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
           the policy

        """
        url = f"{cls.api_url}/policy/api/v1/policytypes/{policy_type.type}/versions/"\
              + f"{policy_type.version}/policies/{policy_name}/versions/{policy_version}"
        policy = cls.send_message_json('GET',
                                       'Get the policy',
                                       url,
                                       basic_auth=basic_auth)
        return policy

    @classmethod
    def create_policy(cls,
                      policy_type: PolicyType,
                      policy_data,
                      basic_auth: Dict[str, str]) -> None:
        """
        Create a policy.

        Args:
           policy_type: the policy type
           type_version: the version of the policy type
           policy_data: the policy to be created, in binary format

        """
        url = f"{cls.api_url}/policy/api/v1/policytypes/{policy_type.type}/"\
              + f"versions/{policy_type.version}/policies"
        cls.send_message('POST',
                         'Create Policy',
                         url,
                         data=policy_data,
                         headers=cls.header,
                         basic_auth=basic_auth)

    @classmethod
    def deploy_policy(cls,
                      policy_data,
                      basic_auth: Dict[str, str]) -> None:
        """
        Deploy a policy.

        Args:
           policy_data: the policy to be deployed, in binary format

        """
        url = f"{cls.pap_url}/policy/pap/v1/pdps/policies"
        cls.send_message('POST',
                         'Deploy Policy',
                         url,
                         data=policy_data,
                         headers=cls.header,
                         basic_auth=basic_auth)
