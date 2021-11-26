#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test A1policymanagement module."""

from unittest import mock
from oransdk.a1policymanagement.a1policymanagement import A1policymanagement

HEADER = {"Accept": "application/json", "Content-Type": "application/json"}
BASE_URL = "http://localhost:8081"

def test_initialization():
    """Class initialization test."""
    a1policymanagement = A1policymanagement()
    assert isinstance(a1policymanagement, A1policymanagement)


@mock.patch.object(A1policymanagement, 'send_message')
def test_check_status(mock_send_message):
    """Test A1policymanagement's class method."""
    A1policymanagement.check_status()
    mock_send_message.assert_called_once_with('GET',
                                              'Get A1 policy management status',
                                              (f"{BASE_URL}/status"))

@mock.patch.object(A1policymanagement, 'send_message_json')
def test_get_policy_types(mock_send_message_json):
    """Test A1policymanagement's class method."""
    A1policymanagement.get_policy_types()
    mock_send_message_json.assert_called_once_with('GET',
                                              'Get all the policy types',
                                              (f"{BASE_URL}/policy_types"))

@mock.patch.object(A1policymanagement, 'send_message_json')
def test_get_policy_type_agent(mock_send_message_json):
    """Test A1policymanagement's class method."""
    A1policymanagement.get_policy_type_agent()
    mock_send_message_json.assert_called_once_with('GET',
                                              'Get all the policy types from policy agent',
                                              (f"{BASE_URL}/a1-policy/v2/policy-types"))

@mock.patch.object(A1policymanagement, 'send_message_json')
def test_get_policy(mock_send_message_json):
    """Test A1policymanagement's class method."""
    A1policymanagement.get_policy("test_id")
    mock_send_message_json.assert_called_once_with('GET',
                                              'Get the policy with policy id',
                                              (f"{BASE_URL}/a1-policy/v2/policies/test_id"))

@mock.patch.object(A1policymanagement, 'send_message')
def test_create_service(mock_send_message):
    """Test A1policymanagement's class method."""
    service_data = {}
    A1policymanagement.create_service(service_data)
    mock_send_message.assert_called_once_with('PUT',
                                              'Create Service',
                                              (f"{BASE_URL}/a1-policy/v2/services"),
                                              data=service_data,
                                              headers=HEADER)

@mock.patch.object(A1policymanagement, 'send_message')
def test_create_policy(mock_send_message):
    """Test A1policymanagement's class method."""
    policy_data = {}
    A1policymanagement.create_policy(policy_data)
    mock_send_message.assert_called_once_with('PUT',
                                              'Create Policy',
                                              (f"{BASE_URL}/a1-policy/v2/policies"),
                                              data=policy_data,
                                              headers=HEADER)
