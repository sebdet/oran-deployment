#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""Module called by pytest."""
import logging
import logging.config
import os
from onapsdk.configuration import settings
from smo.smo import Smo
from smo.network_simulators import NetworkSimulators

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Session setup")

network_sims = NetworkSimulators("./resources")
smo = Smo()

###### Entry points of PYTEST Session
def pytest_sessionstart():
    """Pytest calls it when starting a test session."""
    smo.wait_for_smo_to_be_running()
    ### Due to an Onap Ves/dmaap behavior !!! DU sims must send messages
    ### twice so we need to create/delete the sims
#    network_sims.start_network_simulators()
#    network_sims.wait_for_network_simulators_to_be_running()
#    time.sleep(20)
    ## Now kill the simulators and restart them for the test session
    network_sims.stop_network_simulators()
    ###### END of FIRST start, now we can start the sims for the real tests.
