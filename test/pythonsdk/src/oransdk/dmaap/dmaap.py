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
"""Oran Dmaap module."""

from onapsdk.dmaap.dmaap import Dmaap
from oransdk.configuration import settings

class OranDmaap(Dmaap):
    """Dmaap library provides functions for getting events from Dmaap."""

    base_url = settings.DMAAP_URL
    get_all_topics_url = f"{base_url}/topics/listAll"
    header = {"accept": "application/json", "Content-Type": "application/json"}

    @classmethod
    def create_topic(cls,
                     topic) -> None:
        """
        Create topic in Dmaap.

        Args:
           topic: the topic to create, in json format

        """
        url = f"{cls.base_url}/topics/create"
        cls.send_message('POST',
                         'Create Dmaap Topic',
                         url,
                         data=topic,
                         headers=cls.header)

    @classmethod
    def create_service(cls,
                       service_data) -> None:
        """
        Create Service to policy agent via Dmaap.

        Args:
           service_data: the service data in binary format

        """
        OranDmaap._send_event("A1-POLICY-AGENT-READ", service_data, "Create Service via Dmaap")

    @classmethod
    def send_link_failure_event(cls,
                                event) -> None:
        """
        Send link failure event.

        Args:
           event: the event to sent, in binary format

        """
        OranDmaap._send_event("unauthenticated.SEC_FAULT_OUTPUT", event, "Send link failure event")

    @classmethod
    def get_message_from_topic(cls, topic, timeout, dmaap_group, dmaap_user) -> str:
        """
        Get payload from any topic.

        Returns:
            the result

        """
        url = f"{cls.base_url}/events/{topic}/{dmaap_group}/{dmaap_user}?timeout={timeout}"
        return cls.send_message('GET', 'Get payload of specific topic', url)

    @classmethod
    def get_result(cls) -> str:
        """
        Get result from previous request.

        Returns:
            the result

        """
        topic = "A1-POLICY-AGENT-WRITE"
        url = f"{cls.base_url}/events/{topic}/users/policy-agent?timeout=15000&limit=100"
        result = cls.send_message('GET', 'Get result from previous request', url)
        return result

    @classmethod
    def _send_event(cls,
                    topic,
                    event_data,
                    description) -> None:
        url = f"{cls.base_url}/events/{topic}/"
        cls.send_message('POST',
                         description,
                         url,
                         data=event_data,
                         headers=cls.header)
