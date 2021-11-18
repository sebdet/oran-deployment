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
    HEADER={"accept": "application/json", "Content-Type": "application/json"}

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
                                            headers=cls.HEADER)

    @classmethod
    def create_service(cls,
                    service_data) -> None:
        """
        Create Service to policy agent via Dmaap.

        Args:
           service_data: the service data in binary format

        """
        OranDmaap.__get_events("A1-POLICY-AGENT-READ", service_data, "Create Service via Dmaap")

    @classmethod
    def send_link_failure_event(cls,
                    event) -> None:
        """
        Send link failure event.

        Args:
           event: the event to sent, in binary format

        """
        OranDmaap.__get_events("unauthenticated.SEC_FAULT_OUTPUT", event, "Send link failure event")

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

    @classmethod
    def __send_event(cls,
                   topic,
                   event_data,
                   description) -> None:
        url = f"{DmaapService._url}/events/{topic}/"
        instance_details = cls.send_message('POST',
                                            description,
                                            url,
                                            data=event,
                                            headers=cls.HEADER)
