#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Onap Sdnc module."""
from typing import Dict
from onapsdk.sdnc.sdnc_Element import SdncElement

class OranSdnc(SdncElement):

    @classmethod
    def get_status(cls) -> dict:
        """
        Get status of SDNC component.

        Returns:
           the status of the SDNC component

        """
        url = f"{cls.base_url}/apidoc/explorer/"
        status = cls.send_message('GET',
                                  'Get status of SDNC component',
                                  url)
        return status
