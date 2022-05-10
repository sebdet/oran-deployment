#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test Clamp module."""
from unittest import mock
from oransdk.policy.clamp import ClampToscaTemplate


HEADER = {"Accept": "application/json", "Content-Type": "application/json"}
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}
BASE_URL = "http://localhost:8084"
CLAMP = ClampToscaTemplate(BASIC_AUTH)


def test_initialization():
    """Class initialization test."""
    clamp = ClampToscaTemplate(BASIC_AUTH)
    assert isinstance(clamp, ClampToscaTemplate)


@mock.patch.object(ClampToscaTemplate, 'send_message')
def test_get_template_instance(mock_send_message):
    """Test Clamp's class method."""
    ClampToscaTemplate.get_template_instance(CLAMP)
    url = f"{CLAMP.base_url()}/acm/getToscaInstantiation"
    mock_send_message.assert_called_with('GET',
                                         'Get tosca template instance',
                                         url,
                                         basic_auth=BASIC_AUTH)


@mock.patch.object(ClampToscaTemplate, 'send_message')
def test_upload_commission(mock_send_message):
    """Test Clamp's class method."""
    tosca_template = {}
    ClampToscaTemplate.upload_commission(CLAMP, tosca_template)
    url = f"{CLAMP.base_url()}/acm/commissionToscaTemplate"
    mock_send_message.assert_called_with('POST',
                                         'Upload Tosca to commissioning',
                                         url,
                                         data=tosca_template,
                                         headers=HEADER,
                                         basic_auth=BASIC_AUTH)


@mock.patch.object(ClampToscaTemplate, 'send_message')
def test_create_instance(mock_send_message):
    """Test Clamp's class method."""
    tosca_instance_properties = {}
    ClampToscaTemplate.create_instance(CLAMP, tosca_instance_properties)
    url = f"{CLAMP.base_url()}/acm/postToscaInstanceProperties"
    mock_send_message.assert_called_once_with('POST', 'Create Tosca instance', url, data=tosca_instance_properties,
                                              headers=HEADER, basic_auth=BASIC_AUTH)


@mock.patch.object(ClampToscaTemplate,'send_message')
def test_get_template_instance_status(mock_send_message):
    """Test Clamp's class method."""
    name = ""
    version = ""
    ClampToscaTemplate.get_template_instance_status(CLAMP, name, version)
    url = f"{CLAMP.base_url()}/acm/getInstantiationOrderState?name={name}&version={version}"
    mock_send_message.assert_called_with('GET',
                                         'Get tosca template instance',
                                         url,
                                         basic_auth=BASIC_AUTH)


@mock.patch.object(ClampToscaTemplate, 'send_message')
def test_delete_template_instance(mock_send_message):
    name = ""
    version = ""
    ClampToscaTemplate.delete_template_instance(CLAMP, name, version)
    url = f"{CLAMP.base_url()}/acm/deleteToscaInstanceProperties?name={name}&version={version}"
    mock_send_message.assert_called_with('DELETE', 'Delete the tosca instance', url, headers=HEADER,
                                         basic_auth=BASIC_AUTH)


@mock.patch.object(ClampToscaTemplate, 'send_message')
def test_decommission_template(mock_send_message):
    name = ""
    version = ""
    ClampToscaTemplate.decommission_template(CLAMP, name, version)
    url = f"{CLAMP.base_url()}/acm/decommissionToscaTemplate?name={name}&version={version}"
    mock_send_message.assert_called_with('DELETE', 'Decommission the tosca template', url, headers=HEADER,
                                         basic_auth=BASIC_AUTH)
