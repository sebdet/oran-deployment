#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

"""Smo NonRtric module."""
import logging
import logging.config
from onapsdk.configuration import settings
from waiting import wait
from smo.onap import Onap
from smo.nonrtric import NonRTRic

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Smo k8s")

class Smo():
    """Check SMo nonrtric k8s deployment."""

    onap = Onap()
    non_rt_ric = NonRTRic()

    @classmethod
    def wait_for_smo_to_be_running(cls):
        """Check and wait for the SMo to be running."""
        wait(lambda: cls.onap.is_onap_up() and cls.non_rt_ric.is_nonrtric_up(), sleep_seconds=10, timeout_seconds=300, waiting_for="SMO to be ready")
