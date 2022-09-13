#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2021-2022 AT&T Intellectual Property. All rights
#                             reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END============================================
# ===================================================================
#
###

"""NetworkSimulators module."""
import logging
import logging.config
import json
from subprocess import check_output, run
import sys
import requests
from onapsdk.configuration import settings
from waiting import wait

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Network Simulators k8s")

class NetworkSimulators():
    """Network simulators controls the simulators k8s deployment."""

    resources_path = ""

    def __init__(self, resources_dir):
        """Create NetworkSimulators class."""
        self.resources_path = resources_dir

    def start_network_simulators(self):
        """Start all simulators defined in resources_path."""
        logger.info("Start the network simulators")
        cmd = "kubectl create namespace network"
        check_output(cmd, shell=True).decode('utf-8')
        cmd = f"helm install --debug oran-simulator local/ru-du-simulators --namespace network -f {self.resources_path}/network-simulators-topology/network-simulators-override.yaml -f {self.resources_path}/network-simulators-topology/network-simulators-topology-override.yaml"
        check_output(cmd, shell=True).decode('utf-8')

    def start_and_wait_network_simulators(self):
        """Start and wait for all simulators defined in resources_path."""
        logger.info("Start the network simulators")
        self.start_network_simulators()
        NetworkSimulators.wait_for_network_simulators_to_be_running()

    @staticmethod
    def get_all_simulators():
        """Retrieve all simulators defined in k8s services."""
        dockerFilter = check_output("kubectl get services -n network -o name | awk -F \"/\" '{print $2}'", shell=True)
        return dockerFilter.splitlines()

    @staticmethod
    def stop_network_simulators():
        """Stop the simulators."""
        logger.info("Clean up any network simulators")
        cmd = "kubectl delete namespace network"
        run(cmd, shell=True, check=False)

    @staticmethod
    def is_network_simulators_up() -> bool:
        """Check if the network simulators are up."""
        cmd = "kubectl get pods --field-selector status.phase!=Running -n network"
        result = check_output(cmd, shell=True).decode('utf-8')
        logger.info("Checking if network simulators is UP: %s", result)
        if result == '':
            logger.info("Network sims is Up")
            return True
        logger.info("Network sims is Down")
        return False

    def update_event_settings(self, nfName, nfType):
        """Send one event for specific simulator of a specific type."""
        file = f'{self.resources_path}/faults-config/event-settings-'+nfType+'.json'
        logger.info("Faults parameters path: %s", file)
        with open(file) as json_file:
            body = json.load(json_file)
            url = settings.SDNC_URL + '/rests/data/network-topology:network-topology/topology=topology-netconf/node=' + nfName + '/yang-ext:mount/nts-network-function:simulation/network-function'
            logger.info("Using SDNC URL: %s", url)
            headers = {
                'content-type': 'application/yang-data+json',
                'accept': 'application/yang-data+json',
                'Authorization' : settings.SDNC_AUTH
            }
            try:
                response = requests.put(url, verify=False, json=body, headers=headers)
                logger.info("Response: %s", str(response))
            except requests.exceptions.Timeout:
                sys.exit('HTTP request failed, please check you internet connection.')
            except requests.exceptions.TooManyRedirects:
                sys.exit('HTTP request failed, please check your proxy settings.')
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            return response.status_code >= 200 and response.status_code < 300

    def enable_events_for_all_simulators(self):
        """Send event to sdnc for all sim containers."""
        for container in NetworkSimulators.get_all_simulators():
            name = container.decode("utf-8")
            if "o-" in name:
                if "o-ru" in name:
                    logger.info("Set %s %s", name, self.update_event_settings(name, "ru"))
                if "o-du" in name:
                    logger.info("Set %s %s", name, self.update_event_settings(name, "du"))

    @staticmethod
    def wait_for_network_simulators_to_be_running():
        """Check and wait for the network sims to be running."""
        wait(lambda: NetworkSimulators.is_network_simulators_up(), sleep_seconds=settings.NETWORK_SIMULATOR_CHECK_RETRY, timeout_seconds=settings.NETWORK_SIMULATOR_CHECK_TIMEOUT, waiting_for="Network simulators to be ready")
