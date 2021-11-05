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

    @classmethod
    def create_topic(cls,
                    topic,
                    basic_auth: Dict[str, str]) -> dict:
        """
        Create topic in Dmaap.

        Args:
           topic: the topic to create, in json format
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        """
        create_events_url = f"{DmaapService._url}/topics/create"
        instance_details = cls.send_message('POST',
                                            'Create Dmaap Topic',
                                            create_events_url,
                                            data=topic)

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