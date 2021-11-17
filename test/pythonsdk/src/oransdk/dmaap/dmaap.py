#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Oran Dmaap module."""
from typing import Dict
from onapsdk.dmaap.dmaap import Dmaap
from onapsdk.dmaap.dmaap_service import DmaapService

class OranDmaap(Dmaap):
    """Dmaap library provides functions for getting events from Dmaap."""

    get_all_topics_url = f"{DmaapService._url}/topics/listAll"
    header={"accept: application/json", "Content-Type: application/json"}

    @classmethod
    def create_topic(cls,
                    topic) -> None:
        """
        Create topic in Dmaap.

        Args:
           topic: the topic to create, in json format
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        """
        url = f"{DmaapService._url}/topics/create"
        instance_details = cls.send_message('POST',
                                            'Create Dmaap Topic',
                                            url,
                                            data=topic,
                                            headers=header)

    @classmethod
    def create_service(cls,
                    service_data) -> None:
        """
        Create Service to policy agent via Dmaap.

        Args:
           service_data: the service data in binary format

        """
        url = f"{DmaapService._url}/events/A1-POLICY-AGENT-READ/"
        instance_details = cls.send_message('POST',
                                            'Create Service via Dmaap',
                                            url,
                                            data=service_data,
                                            headers=header)

    @classmethod
    def get_result(cls) -> str:
        """
        Get result from previous request.

        Returns:
            the result

        """
        url = f"{url}/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100"
        result = cls.send_message('GET',
                                   'Get result from previous request',
                                    url)
        return result

    @classmethod
    def get_all_topics(cls,
                       basic_auth: Dict[str, str]) -> dict:
        """
        Get all topics stored in Dmaap.

        Args:
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
            (dict) Topics from Dmaap

        """
        return super().get_all_topics(basic_auth)