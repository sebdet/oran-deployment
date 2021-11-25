#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Oran A1 Simulator module."""

from onapsdk.onap_service import OnapService

class A1sim(OnapService):
    """Oran A1 Simulator library."""

    @classmethod
    def check_version(cls, base_url) -> str:
        """
        Return ric version.

        Args:
           base_url: the base url of the ric

        Returns:
            the ric version

        """
        url = f"{base_url}/counter/interface"
        version = cls.send_message('GET',
                                   'Get ric version',
                                   url)
        return version

    @classmethod
    def check_status(cls, url) -> str:
        """
        Return ric status.

        Args:
           url: the url of the ric

        Returns:
            the ric status

        """
        url = f"{url}"
        status = cls.send_message('GET',
                                  'Get ric status',
                                  url)
        return status

    @classmethod
    def get_policy_number(cls, url) -> str:
        """
        Policy numbers for ric.

        Args:
           url: the url of the ric

        Returns:
            the policy numbers for ric

        """
        url = f"{url}/counter/num_instances"
        policy_number = cls.send_message('GET',
                                         'Get policy numbers for ric',
                                         url)
        return policy_number

    @classmethod
    def create_policy_type(cls,
                           url,
                           policy_type_id,
                           policy_type_data) -> None:
        """
        Create topic in Dmaap.

        Args:
           url: the url of the ric
           policy_type_num: the policy type id
           policy_type_data: the policy type data in binary format

        """
        url = f"{url}/policytype?id={policy_type_id}"
        cls.send_message('PUT',
                         'Create Policy Type',
                         url,
                         data=policy_type_data,
                         headers={"Accept":"application/json", "Content-Type":"application/json"})
