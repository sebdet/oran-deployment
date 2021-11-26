#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test A1sim module."""

from unittest import mock
from oransdk.a1sim.a1sim import A1sim

HEADER = {"Accept": "application/json", "Content-Type": "application/json"}
BASE_URL = "http://localhost:8081"

def test_initialization():
    """Class initialization test."""
    a1sim = A1sim()
    assert isinstance(a1sim, A1sim)


@mock.patch.object(A1sim, 'send_message')
def test_check_version(mock_send_message):
    """Test A1sim's class method."""
    A1sim.check_version(BASE_URL)
    mock_send_message.assert_called_once_with('GET',
                                              'Get ric version',
                                              (f"{BASE_URL}/counter/interface"))

@mock.patch.object(A1sim, 'send_message')
def test_check_status(mock_send_message):
    """Test A1sim's class method."""
    A1sim.check_status(BASE_URL)
    mock_send_message.assert_called_once_with('GET',
                                              'Get ric status',
                                              (f"{BASE_URL}"))

@mock.patch.object(A1sim, 'send_message')
def test_get_policy_number(mock_send_message):
    """Test A1sim's class method."""
    A1sim.get_policy_number(BASE_URL)
    mock_send_message.assert_called_once_with('GET',
                                              'Get policy numbers for ric',
                                              (f"{BASE_URL}/counter/num_instances"))

@mock.patch.object(A1sim, 'send_message')
def test_create_policy_type(mock_send_message):
    """Test A1sim's class method."""
    A1sim.create_policy_type(BASE_URL, "test_id", {})
    mock_send_message.assert_called_once_with('PUT',
                                              'Create Policy Type',
                                              (f"{BASE_URL}/policytype?id=test_id"),
                                              data={},
                                              headers=HEADER)
