import pytest
import logging
import logging.config
from subprocess import check_output, run
import time
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import os
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
def pytest_sessionstart(session):

    smo.wait_for_smo_to_be_running()
    ### Due to an Onap Ves bugs and dmaap init !!! DU sims must send messages twice so we need to create/delete the sims
    network_sims.start_network_simulators()
    network_sims.wait_for_network_simulators_to_be_running()
    time.sleep(3)
    dmaap = OranDmaap()
    # Do a first get to register the o1test/o1test user in DMAAP,
    # all registration messages will then be stored for the tests.
    dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 1000, settings.DMAAP_GROUP, settings.DMAAP_USER)
    ## Now kill the simulators and restart them for the test session
    network_sims.stop_network_simulators()
    ###### END of FIRST start, now we can start the sims for the real tests.

def pytest_sessionfinish(session, exitstatus):
    network_sims.stop_network_simulators()
    logger.info ("Test Session cleanup done")
