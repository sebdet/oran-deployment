#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

"""Oran O1 Simulatorn Module"""

from onapsdk.onap_service import OnapService
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.configuration import settings


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











