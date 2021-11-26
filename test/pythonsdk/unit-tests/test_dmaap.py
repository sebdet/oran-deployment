#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test clamp module."""

from unittest import mock
from oransdk.dmaap.dmaap import OranDmaap
from onapsdk.dmaap.dmaap_service import DmaapService

#examples
TOPIC = {
    "topicName": "test.TOPIC",
    "topicDescription": "test topic",
    "partitionCount": 1,
    "replicationCnCount": 1,
    "transactionEnabled": "false"
    }

HEADER={"accept": "application/json", "Content-Type": "application/json"}
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}
BASE_URL = "http://localhost:3904"

def test_initialization():
    """Class initialization test."""
    dmaap = OranDmaap()
    assert isinstance(dmaap, OranDmaap)


@mock.patch.object(OranDmaap, 'send_message')
def test_create_topic(mock_send_message):
    """Test Dmaap's class method."""
    OranDmaap.create_topic(TOPIC)
    mock_send_message.assert_called_once_with('POST',
                                              'Create Dmaap Topic',
                                              (f"{BASE_URL}/topics/create"),
                                              data=TOPIC,
                                              headers=HEADER)

@mock.patch.object(OranDmaap, 'send_message')
def test_create_service(mock_send_message):
    """Test Dmaap's class method."""
    event = {}
    OranDmaap.create_service(event)
    mock_send_message.assert_called_once_with('POST',
                                              'Create Service via Dmaap',
                                              (f"{BASE_URL}/events/A1-POLICY-AGENT-READ/"),
                                              data=event,
                                              headers=HEADER)

@mock.patch.object(OranDmaap, 'send_message')
def test_send_link_failure_event(mock_send_message):
    """Test Dmaap's class method."""
    event = {}
    OranDmaap.send_link_failure_event(event)
    mock_send_message.assert_called_once_with('POST',
                                              'Send link failure event',
                                              (f"{BASE_URL}/events/unauthenticated.SEC_FAULT_OUTPUT/"),
                                              data=event,
                                              headers=HEADER)

@mock.patch.object(OranDmaap, 'send_message')
def test_get_result(mock_send_message):
    """Test Dmaap's class method."""
    OranDmaap.get_result()
    mock_send_message.assert_called_once_with('GET',
                                              'Get result from previous request',
                                              (f"{BASE_URL}/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100"))

@mock.patch.object(OranDmaap, 'send_message_json')
def test_get_all_topics(mock_send_message_json):
    """Test Dmaap's class method."""
    assert OranDmaap.get_all_topics_url == f"{BASE_URL}/topics/listAll"
