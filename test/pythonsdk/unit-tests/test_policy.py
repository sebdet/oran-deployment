#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test Policy module."""

from unittest import mock
from oransdk.policy.policy import OranPolicy, PolicyType

HEADER = {"Accept": "application/json", "Content-Type": "application/json"}
API_URL = "https://localhost:6969"
PAP_URL = "https://localhost:6969"
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}

def test_initialization():
    """Class initialization test."""
    policy = OranPolicy()
    assert isinstance(policy, OranPolicy)


@mock.patch.object(OranPolicy, 'send_message_json')
def test_get_components_status(mock_send_message_json):
    """Test Policy's class method."""
    OranPolicy.get_components_status(BASIC_AUTH)
    mock_send_message_json.assert_called_once_with('GET',
                                                   'Get status of Policy component',
                                                   (f"{PAP_URL}/policy/pap/v1/components/healthcheck"),
                                                   basic_auth=BASIC_AUTH)

@mock.patch.object(OranPolicy, 'send_message_json')
def test_get_policy_status(mock_send_message_json):
    """Test Policy's class method."""
    OranPolicy.get_policy_status(BASIC_AUTH)
    mock_send_message_json.assert_called_once_with('GET',
                                                   'Get status of all the policies',
                                                   (f"{PAP_URL}/policy/pap/v1/policies/status"),
                                                   basic_auth=BASIC_AUTH)


@mock.patch.object(OranPolicy, 'send_message')
def test_get_policy(mock_send_message):
    """Test Policy's class method."""
    OranPolicy.get_policy(PolicyType(type="test_type", version="type_version"),
                          "policy_name", "policy_version", BASIC_AUTH)
    mock_send_message.assert_called_once_with('GET',
                                                   'Get the policy',
                                                   (f"{API_URL}/policy/api/v1/policytypes/test_type/versions/"\
                                                   + "type_version/policies/policy_name/versions/policy_version"),
                                                   basic_auth=BASIC_AUTH)


@mock.patch.object(OranPolicy, 'send_message')
def test_create_policy(mock_send_message):
    """Test Policy's class method."""
    OranPolicy.create_policy(PolicyType(type="test_type", version="type_version"), {}, BASIC_AUTH)
    mock_send_message.assert_called_once_with('POST',
                                              'Create Policy',
                                              (f"{API_URL}/policy/api/v1/policytypes/test_type/"\
                                              + "versions/type_version/policies"),
                                              data={},
                                              headers=HEADER,
                                              basic_auth=BASIC_AUTH)

@mock.patch.object(OranPolicy, 'send_message')
def test_deploy_policy(mock_send_message):
    """Test Policy's class method."""
    OranPolicy.deploy_policy({}, BASIC_AUTH)
    mock_send_message.assert_called_once_with('POST',
                                              'Deploy Policy',
                                              (f"{API_URL}/policy/pap/v1/pdps/policies"),
                                              data={},
                                              headers=HEADER,
                                              basic_auth=BASIC_AUTH)

@mock.patch.object(OranPolicy, 'send_message')
def test_undeploy_policy(mock_send_message):
    """Test Policy's class method."""
    OranPolicy.undeploy_policy("policy_id","1.0.0", BASIC_AUTH)
    mock_send_message.assert_called_once_with('DELETE',
                                              'Undeploy Policy',
                                              (f"{PAP_URL}/policy/pap/v1/pdps/policies/policy_id/versions/1.0.0"),
                                              headers=HEADER,
                                              basic_auth=BASIC_AUTH)

@mock.patch.object(OranPolicy, 'send_message')
def test_delete_policy(mock_send_message):
    """Test Policy's class method."""
    OranPolicy.delete_policy(PolicyType(type="test_type", version="type_version"), "policy_id","1.0.0", BASIC_AUTH)
    mock_send_message.assert_called_once_with('DELETE',
                                              'Delete Policy',
                                              (f"{API_URL}/policy/api/v1/policytypes/test_type/versions/type_version/policies/policy_id/versions/1.0.0"),
                                              headers=HEADER,
                                              basic_auth=BASIC_AUTH)
