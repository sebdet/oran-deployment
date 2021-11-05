#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Oran A1 Simulator module."""

from onapsdk.onap_service import OnapService

class A1sim(OnapService):

    @classmethod
    def check_version(cls, url) -> str:
        """
        Return ric version.

        Returns:
            the ric version

        """
        url = f"{url}/counter/interface"
        version = cls.send_message('GET',
                                   'Get ric version',
                                    url)
        return version
