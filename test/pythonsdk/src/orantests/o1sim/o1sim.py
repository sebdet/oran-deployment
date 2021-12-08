#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

"""Oran O1 Simulatorn Module"""

from onapsdk.onap_service import OnapService

class O1sim(OnapService):

        @classmethod
        def check_status(cls, url) -> str:
            """

            Return o1 status.

            Args:
               url: the url of the o1

            Returns:
                the o1 status


            """
            url = f"{url}"
            status = cls.send_message('GET',

                                       'Get o1 status',
                                        url)
            return status

             @classmethod
                def create_device_type(cls,
                                       url,
                                       device_type_id,
                                       device_type_data) -> None:
                    """
                    Create topic in o1.
                    Args:
                       url: the url of the o1
                       device_type_num: the device type id
                       device_type_data: the device type data in binary format
                    """
                    url = f"{url}/devicetype?id={device_type_id}"
                    cls.send_message('PUT',
                                     'Create Device Type',
                                     url,
                                     data=device_type_data,
                                     headers={"Accept":"application/json", "Content-Type":"application/json"})

              @classmethod
                 def get_device_status(cls,
                                        device_node,
                                        basic_auth: Dict[str, str]) -> dict:
                     """
                     Get status of the device.

                     Args:
                        basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

                     Returns:
                        the status of the device

                     """
                     url = f"{cls.base_url}/rests/operations/data-provider:read-network-element-connection-list"\
                           + f"/node={node-id}/yang-ext:mount/"
                     status = cls.send_message_json('GET',
                                                    'Get status of device connectivity',
                                                    url,
                                                    basic_auth=basic_auth)
                     return status


              @classmethod
                 def get_fault_status(cls,
                                        fault_node,
                                        basic_auth: Dict[str, str]) -> dict:
                     """
                     Get status of the fault.

                     Args:
                        basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

                     Returns:
                        the status of the fault

                     """
                     url = f"{cls.base_url}/rests/operations/data-provider:read-network-status"\
                           + f"/node={node-id}/yang-ext:mount/"
                     status = cls.send_message_json('GET',
                                                    'Get status of device connectivity',
                                                    url,
                                                    basic_auth=basic_auth)
                     return status
                     

