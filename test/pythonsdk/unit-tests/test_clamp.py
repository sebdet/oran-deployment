#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test Clamp module."""

from unittest import mock
from oransdk.policy.clamp import OranClamp


HEADER={"accept": "application/json", "Content-Type": "application/json"}
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}
BASE_URL = "http://localhost:8084"

def test_initialization():
    """Class initialization test."""
    clamp = OranClamp()
    assert isinstance(clamp, OranClamp)

@mock.patch.object(OranClamp, 'send_message')
def test_upload_commission(mock_send_message):
    """Test Clamp's class method."""
    OranClamp.upload_commission(BASIC_AUTH)
    url = f"{BASE_URL}/clamp/restservices/clds/v2/toscaControlLoop/commissionToscaTemplate"
    mock_send_message.assert_called_once_with('POST', 'Upload commission', url, basic_auth=BASIC_AUTH)

@mock.patch.object(OranClamp, 'send_message')
def test_create_instance(mock_send_message):
    """Test Clamp's class method."""
    dataclamp = {}
    OranClamp.create_instance(dataclamp, BASIC_AUTH)
    url = f"{BASE_URL}/restservices/clds/v2/toscaControlLoop/postToscaInstanceProperties"
    mock_send_message.assert_called_once_with('POST', 'Create Instance', url, data=dataclamp, headers=HEADER, basic_auth=BASIC_AUTH)

@mock.patch.object(OranClamp, 'send_message')
def test_change_instance_status(mock_send_message):
    dataclamp={}
    OranClamp.change_instance_status(dataclamp)
    url = f"{BASE_URL}/restservices/clds/v2/toscaControlLoop/putToscaInstantiationStateChange"
    mock_send_message.assert_called_once_with('PUT', 'Change instance', url, data=dataclamp, headers=HEADER)

@mock.patch.object(OranClamp, 'send_message')
def test_delete_instance(mock_send_message):
    OranClamp.delete_instance()
    url = f"{BASE_URL}/restservices/clds/v2/toscaControlLoop/deleteToscaInstanceProperties?name=PMSH_Instance1&version=1.2.3"
    mock_send_message.assert_called_with('DELETE', 'Delete instance', url, headers=HEADER)

@mock.patch.object(OranClamp, 'send_message')
def test_decommission_template(mock_send_message):
    OranClamp.decommission_template()
    url = f"{BASE_URL}/restservices/clds/v2/toscaControlLoop/decommissionToscaTemplate?name=ToscaServiceTemplateSimple&version=1.0.0"
    mock_send_message.assert_called_with('DELETE', 'Decommision template', url, headers=HEADER)
