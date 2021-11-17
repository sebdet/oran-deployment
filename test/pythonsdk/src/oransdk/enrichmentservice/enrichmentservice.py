#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Oran Enrichment Service module."""

from onapsdk.onap_service import OnapService

class EnrichmentService(OnapService):

    base_url: str = settings.EMS_URL
    ems_header={"Content-Type": "application/json"}

    @classmethod
    def check_status(cls) -> str:
        """
        Get the status of the EnrichmentService component.

        Returns:
            the status of the EnrichmentService component

        """
        url = f"{base_url}/status"
        status = cls.send_message('GET',
                                   'Get EMS status',
                                    url)
        return status

    @classmethod
    def get_eitypes(cls) -> str:
        """
        Get all the EiTypes.

        Returns:
            the list of EiTypes

        """
        url = f"{base_url}/data-producer/v1/info-types"
        eitypes = cls.send_message('GET',
                                   'Get all the EiTypes',
                                    url,
                                    headers=ems_header)
        return eitypes

    @classmethod
    def get_eitype_individual(cls, type) -> str:
        """
        Get individual EiType.

        Args:
           type: the EiType name

        Returns:
            the details of the EiType

        """
        url = f"{base_url}/data-producer/v1/info-types/{type}"
        eitype = cls.send_message('GET',
                                   'Get individual EiType',
                                    url,
                                    headers=ems_header)
        return eitype

    @classmethod
    def get_eiproducers(cls) -> str:
        """
        Get all the EiProducers.

        Returns:
            the list of EiProducers

        """
        url = f"{base_url}/data-producer/v1/info-producers"
        eitypes = cls.send_message('GET',
                                   'Get all the EiProducers',
                                    url,
                                    headers=ems_header)
        return eitypes

    @classmethod
    def get_eiproducer_individual(cls, producer) -> str:
        """
        Get individual EiProducer.

        Args:
           type: the EiProducer name

        Returns:
            the details of the EiProducer

        """
        url = f"{base_url}/data-producer/v1/info-producers/{producer}"
        eiproducer = cls.send_message('GET',
                                   'Get individual EiProducer',
                                    url,
                                    headers=ems_header)
        return eiproducer

    @classmethod
    def get_eiproducer_status(cls, producer) -> str:
        """
        Get the status of EiProducer.

        Args:
           type: the EiProducer name

        Returns:
            the status of the EiProducer

        """
        url = f"{base_url}/data-producer/v1/info-producers/{producer}/status"
        status = cls.send_message('GET',
                                   'Get the status of EiProducer',
                                    url,
                                    headers=ems_header)
        return status

    @classmethod
    def get_eijobs(cls) -> str:
        """
        Get all the EiJobs.

        Returns:
            the list of EiJobs

        """
        url = f"{base_url}/A1-EI/v1/eijobs"
        eijobs = cls.send_message('GET',
                                   'Get all the EiJobs',
                                    url,
                                    headers=ems_header)
        return eijobs

    @classmethod
    def get_eijob_individual(cls, job) -> str:
        """
        Get individual EiJob.

        Args:
           type: the EiJob name

        Returns:
            the details of the EiJob

        """
        url = f"{base_url}/A1-EI/v1/eijobs/{job}"
        eijob = cls.send_message('GET',
                                 'Get individual EiJob',
                                 url,
                                 headers=ems_header)
        return eijob

    @classmethod
    def create_eitype(cls,
                    type,
                    type_data) -> None:
        """
        Create EiType.

        Args:
           type: the EiType name
           type_data: the EiType data to create, in binary format

        """
        url = f"{base_url}/data-producer/v1/info-types/{type}"
        instance_details = cls.send_message('PUT',
                                            'Create EiType',
                                            url,
                                            data=type_data,
                                            headers=ems_header)

    @classmethod
    def create_eiproducer(cls,
                    producer,
                    producer_data) -> None:
        """
        Create EiProducer.

        Args:
           producer: the EiProducer name
           producer_data: the EiProducer data to create, in binary format

        """
        url = f"{base_url}/data-producer/v1/info-producers/{producer}"
        instance_details = cls.send_message('PUT',
                                            'Create EiProducer',
                                            url,
                                            data=producer_data,
                                            headers=ems_header)

    @classmethod
    def create_eitype(cls,
                    job,
                    job_data) -> None:
        """
        Create EiJob.

        Args:
           job: the EiJob name
           job_data: the EiJob data to create, in binary format

        """
        url = f"{base_url}/A1-EI/v1/eijobs/{type}"
        instance_details = cls.send_message('PUT',
                                            'Create EiJob',
                                            url,
                                            data=job_data,
                                            headers=ems_header)