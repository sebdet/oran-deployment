#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test OranSdnc module."""

from unittest import mock
from oransdk.sdnc.sdnc import OranSdnc

BASE_URL = "http://localhost:8282"
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}
HEADER = {"Accept": "application/json", "Content-Type": "application/json"}
def test_initialization():
    """Class initialization test."""
    sdnc = OranSdnc()
    assert isinstance(sdnc, OranSdnc)


@mock.patch.object(OranSdnc, 'send_message')
def test_get_status(mock_send_message):
    """Test Sdnc's class method."""
    OranSdnc.get_status()
    mock_send_message.assert_called_once_with('GET',
                                              'Get status of SDNC component',
                                              (f"{BASE_URL}/apidoc/explorer/"))

@mock.patch.object(OranSdnc, 'send_message_json')
def test_get_odu_oru_status(mock_send_message_json):
    """Test Sdnc's class method."""
    OranSdnc.get_odu_oru_status("o-du", "radio21", BASIC_AUTH)
    mock_send_message_json.assert_called_once_with('GET',
                                                   'Get status of Odu connectivity',
                                                   (f"{BASE_URL}/rests/data/network-topology:network-topology/topology=topology-netconf/node=o-du/yang-ext:mount/o-ran-sc-du-hello-world:network-function/distributed-unit-functions=o-du/radio-resource-management-policy-ratio=radio21"),
                                                   basic_auth=BASIC_AUTH)
@mock.patch.object(OranSdnc, 'send_message')
def test_get_devices(mock_send_message):
    """Test Sdnc's class method."""
    OranSdnc.get_devices("device", BASIC_AUTH)
    mock_send_message.assert_called_with('GET', 'Get status of Device connectivity',
                                              (f"{BASE_URL}/rests/data/network-topology:network-topology/topology=topology-netconf/node=device"), basic_auth=BASIC_AUTH)
@mock.patch.object(OranSdnc, 'send_message')
def test_get_events(mock_send_message):
    """Test Sdnc's class method."""
    OranSdnc.get_events(BASIC_AUTH, "device")
    data = '{"input": {"filter": [ {"property": "node-id", "filtervalue": "device"}],"sortorder":[{"property": "timestamp","sortorder": "descending"}],"pagination": {"size": 10,"page": 1}}}'
    mock_send_message.assert_called_with('POST', 'Get SDNC events',
                                         (f"{BASE_URL}/rests/operations/data-provider:read-faultlog-list"), data=data, headers=HEADER, basic_auth=BASIC_AUTH)
