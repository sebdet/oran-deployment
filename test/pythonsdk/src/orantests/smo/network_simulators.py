#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging
import logging.config
from onapsdk.configuration import settings
from waiting import wait
from subprocess import check_output, run
import json
import requests

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Network Simulators k8s")

class NetworkSimulators():

    resources_path = ""

    def __init__(self, resources_dir):
        self.resources_path = resources_dir

    def start_network_simulators(self):
        logger.info ("Using the topology located in "+self.resources_path)
        logger.info ("Clean up any network simulators")
        cmd="kubectl delete namespace network"
        run(cmd, shell=True, check=False)
        logger.info ("Start the network simulators")
        cmd="kubectl create namespace network"
        check_output(cmd, shell=True).decode('utf-8')
        cmd=f"helm install --debug oran-simulator local/ru-du-simulators --namespace network -f {self.resources_path}/network-simulators-topology/network-simulators-override.yaml -f {self.resources_path}/network-simulators-topology/network-simulators-topology-override.yaml"
        check_output(cmd, shell=True).decode('utf-8')

    def get_all_simulators(self):
        dockerFilter = check_output("kubectl get services -n network -o name | awk -F \"/\" '{print $2}'", shell=True)
        return dockerFilter.splitlines()

    def stop_network_simulators(self):
        cmd="kubectl delete namespace network"
        return check_output(cmd, shell=True).decode('utf-8')

    def is_network_simulators_up(self):
        cmd="kubectl get pods --field-selector status.phase!=Running -n network"
        result=check_output(cmd, shell=True).decode('utf-8')
        logger.info (f"Checking if network simulators is UP:{result}")
        if "" == result:
            logger.info ("Network sims is Up")
            return True
        else:
            logger.info ("Network sims is Down")
            return False

    def update_event_settings(self, nfName, nfType):
        file = f'{self.resources_path}/faults-config/event-settings-'+nfType+'.json'
        print ("File name:" + file)
        with open(file) as json_file:
            body = json.load(json_file)
            url = settings.SDNC_URL + '/rests/data/network-topology:network-topology/topology=topology-netconf/node=' + nfName + '/yang-ext:mount/nts-network-function:simulation/network-function'
            print ("url:"+url)
            headers = {
                'content-type': 'application/yang-data+json',
                'accept': 'application/yang-data+json',
                'Authorization' : settings.SDNC_AUTH
            }
            try:
                response = requests.put(url, verify=False, json=body, headers=headers)
                print("Response:" + str(response))
            except requests.exceptions.Timeout:
                sys.exit('HTTP request failed, please check you internet connection.')
            except requests.exceptions.TooManyRedirects:
                sys.exit('HTTP request failed, please check your proxy settings.')
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            return response.status_code >= 200 and response.status_code < 300

    def enable_events_for_all_simulators(self):
        for container in self.get_all_simulators():
            name = container.decode("utf-8")
            if "o-" in name:
                if "o-ru" in name:
                    print("Set", name, self.update_event_settings(name, "ru"))
                if "o-du" in name:
                    print("Set", name, self.update_event_settings(name, "du"))

    def wait_for_network_simulators_to_be_running(self):
        wait(lambda: self.is_network_simulators_up(), sleep_seconds=10, timeout_seconds=60, waiting_for="Network simulators to be ready")
