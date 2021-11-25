#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""ONAP A1 Policy Management."""

from typing import Dict
from oransdk.configuration import settings
from onapsdk.onap_service import OnapService

class A1policymanagement(OnapService):
    """A1 Policy Management library."""

    base_url = settings.A1_POLICY_MANAGEMENT_URL
    header = {"Accept":"application/json", "Content-Type":"application/json"}

    @classmethod
    def check_status(cls) -> str:
        """
        Get the status of the A1 policy management component.

        Returns:
            the status of the A1 policy management component

        """
        url = f"{cls.base_url}/status"
        status = cls.send_message('GET',
                                  'Get A1 policy management status',
                                  url)
        return status

    @classmethod
    def get_policy_types(cls) -> Dict:
        """
        Get all the policy types.

        Returns:
            the list of policy types

        """
        url = f"{cls.base_url}/policy_types"
        policy_types = cls.send_message_json('GET',
                                             'Get all the policy types',
                                             url)
        return policy_types

    @classmethod
    def get_policy_type_agent(cls) -> Dict:
        """
        Get all the policy types from policy agent.

        Returns:
            the list of policy types

        """
        url = f"{cls.base_url}/a1-policy/v2/policy-types"
        policy_types = cls.send_message_json('GET',
                                             'Get all the policy types from policy agent',
                                             url)
        return policy_types

    @classmethod
    def get_policy(cls, policy_id) -> Dict:
        """
        Get policy.

        Args:
           type: the policy id

        Returns:
            the details of the policy

        """
        url = f"{cls.base_url}/a1-policy/v2/policies/{policy_id}"
        policy = cls.send_message_json('GET',
                                       'Get the policy with policy id',
                                       url)
        return policy


    @classmethod
    def create_service(cls,
                       service_data) -> None:
        """
        Create service.

        Args:
           service_data: the service data in binary format

        """
        url = f"{cls.base_url}/a1-policy/v2/services"
        cls.send_message('PUT',
                         'Create Service',
                         url,
                         data=service_data,
                         headers=cls.header)

    @classmethod
    def create_policy(cls,
                      policy_data) -> None:
        """
        Create policy.

        Args:
           policy_data: the policy data in binary format

        """
        url = f"{cls.base_url}/a1-policy/v2/policies"
        cls.send_message('PUT',
                         'Create Policy',
                         url,
                         data=policy_data,
                         headers=cls.header)
