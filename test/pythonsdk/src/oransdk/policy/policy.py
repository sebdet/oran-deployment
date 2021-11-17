#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Onap Policy module."""

from onapsdk.onap_service import OnapService
from onapsdk.configuration import settings

class OranPolicy(OnapService):

    pap_url: str = settings.POLICY_PAP_URL
    api_url: str = settings.POLICY_API_URL
    header={"accept: application/json", "Content-Type: application/json"}

    @classmethod
    def get_status(cls) -> str:
        """
        Get status of Policy component.

        Returns:
           the status of the Policy component

        """
        url = f"{pap_url}/policy/pap/v1/components/healthcheck"
        status = cls.send_message('GET',
                                  'Get status of Policy component',
                                  url)
        return status

    @classmethod
    def get_policy_status(cls) -> str:
        """
        Get status of all the policies.

        Returns:
           the status of all the policies

        """
        url = f"{pap_url}/policy/pap/v1/policies/status"
        status = cls.send_message('GET',
                                  'Get status of all the policies',
                                  url)
        return status

    @classmethod
    def get_policy(cls,
                   policy_type,
                   type_version,
                   policy_name,
                   policy_version,
                   basic_auth: Dict[str, str]) -> dict:
        """
        Get the policy.

        Args:
           policy_type: the policy type
           type_version: the version of the policy type
           policy_name: the policy name
           policy_version: the version of the policy
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
           the policy

        """
        url = f"{api_url}/policy/api/v1/policytypes/{policy_type}/versions/{type_version}/policies/{policy_name}/versions/{policy_version}"
        policy = cls.send_message('GET',
                                  'Get the policy',
                                  url,
                                  basic_auth=basic_auth)
        return policy

    @classmethod
    def create_policy(cls,
                    policy_type,
                    type_version,
                    policy_data,
                    basic_auth: Dict[str, str]) -> None:
        """
        Create a policy.

        Args:
           policy_type: the policy type
           type_version: the version of the policy type
           policy_data: the policy to be created, in binary format

        """
        url = f"{api_url}/policy/api/v1/policytypes/{policy_type}/versions/{type_version}/policies"
        instance_details = cls.send_message('POST',
                                            'Create Policy',
                                            url,
                                            data=policy_data,
                                            headers=header,
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
        url = f"{pap_url}/policy/pap/v1/pdps/policie"
        instance_details = cls.send_message('POST',
                                            'Deploy Policy',
                                            url,
                                            data=policy_data,
                                            headers=header,
                                            basic_auth=basic_auth)