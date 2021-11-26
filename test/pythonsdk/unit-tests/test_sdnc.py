#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test OranSdnc module."""

from unittest import mock
from oransdk.sdnc.sdnc import OranSdnc

BASE_URL = "http://localhost:8282"
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}

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
    OranSdnc.get_odu_oru_status("o-du", "o-ru", BASIC_AUTH)
    mock_send_message_json.assert_called_once_with('GET',
                                                   'Get status of Odu Oru connectivity',
                                                   (f"{BASE_URL}/rests/data/network-topology:network-topology/"\
                                                   + "topology=topology-netconf/node=o-du/yang-ext:mount/"\
                                                   + "o-ran-sc-du-hello-world:network-function/du-to-ru-connection=o-ru"),
                                                   basic_auth=BASIC_AUTH)
