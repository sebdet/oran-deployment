#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test Enrichment Service module."""

from unittest import mock
from oransdk.enrichmentservice.enrichmentservice import EnrichmentService

HEADER = {"Content-Type": "application/json"}
BASE_URL = "http://localhost:8083"

def test_initialization():
    """Class initialization test."""
    ems = EnrichmentService()
    assert isinstance(ems, EnrichmentService)


@mock.patch.object(EnrichmentService, 'send_message')
def test_check_status(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.check_status()
    mock_send_message.assert_called_once_with('GET',
                                              'Get EMS status',
                                              (f"{BASE_URL}/status"))


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eitypes(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eitypes()
    mock_send_message.assert_called_once_with('GET',
                                              'Get all the EiTypes',
                                              (f"{BASE_URL}/data-producer/v1/info-types"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eitype_individual(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eitype_individual("test_eitype")
    mock_send_message.assert_called_once_with('GET',
                                              'Get individual EiType',
                                              (f"{BASE_URL}/data-producer/v1/info-types/test_eitype"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eiproducers(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eiproducers()
    mock_send_message.assert_called_once_with('GET',
                                              'Get all the EiProducers',
                                              (f"{BASE_URL}/data-producer/v1/info-producers"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eiproducer_individual(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eiproducer_individual("test_producer")
    mock_send_message.assert_called_once_with('GET',
                                              'Get individual EiProducer',
                                              (f"{BASE_URL}/data-producer/v1/info-producers/test_producer"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eiproducer_status(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eiproducer_status("test_producer")
    mock_send_message.assert_called_once_with('GET',
                                              'Get the status of EiProducer',
                                              (f"{BASE_URL}/data-producer/v1/info-producers/test_producer/status"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eijobs(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eijobs()
    mock_send_message.assert_called_once_with('GET',
                                              'Get all the EiJobs',
                                              (f"{BASE_URL}/A1-EI/v1/eijobs"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_get_eijob_individual(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.get_eijob_individual("test_job")
    mock_send_message.assert_called_once_with('GET',
                                              'Get individual EiJob',
                                              (f"{BASE_URL}/A1-EI/v1/eijobs/test_job"),
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_create_eitype(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.create_eitype("type_name", {})
    mock_send_message.assert_called_once_with('PUT',
                                              'Create EiType',
                                              (f"{BASE_URL}/data-producer/v1/info-types/type_name"),
                                              data={},
                                              headers=HEADER)


@mock.patch.object(EnrichmentService, 'send_message')
def test_create_eiproducer(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.create_eiproducer("producer", {})
    mock_send_message.assert_called_once_with('PUT',
                                              'Create EiProducer',
                                              (f"{BASE_URL}/data-producer/v1/info-producers/producer"),
                                              data={},
                                              headers=HEADER)

@mock.patch.object(EnrichmentService, 'send_message')
def test_create_eijob(mock_send_message):
    """Test EnrichmentService's class method."""
    EnrichmentService.create_eijob("job", {})
    mock_send_message.assert_called_once_with('PUT',
                                              'Create EiJob',
                                              (f"{BASE_URL}/A1-EI/v1/eijobs/job"),
                                              data={},
                                              headers=HEADER)
