import pytest
import logging
import logging.config
from subprocess import check_output, run
from waiting import wait
import time
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
import os
import json
import requests

resources_path="./resources"

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("Test Session setup")


def start_network_simulators():
	logger.info ("Clean up any network simulators")
	cmd="kubectl delete namespace network"
	run(cmd, shell=True, check=False)
	logger.info ("Start the network simulators")
	cmd="kubectl create namespace network"
	check_output(cmd, shell=True).decode('utf-8')
	cmd=f"helm install --debug oran-simulator local/ru-du-simulators --namespace network -f {resources_path}/network-simulators-topology/network-simulators-override.yaml -f {resources_path}/network-simulators-topology/network-simulators-topology-override.yaml"
	check_output(cmd, shell=True).decode('utf-8')

def get_all_simulators():
	dockerFilter = check_output("kubectl get services -n network -o name | awk -F \"/\" '{print $2}'", shell=True)
	return dockerFilter.splitlines()

def stop_network_simulators():
	cmd="kubectl delete namespace network"
	return check_output(cmd, shell=True).decode('utf-8')

def is_network_simulators_up():
	cmd="kubectl get pods --field-selector status.phase!=Running -n network"
	result=check_output(cmd, shell=True).decode('utf-8')
	logger.info (f"Checking if network simulators is UP:{result}")
	if "" == result:
		logger.info ("Network sims is Up")
		return True
	else:
		logger.info ("Network sims is Down")
		return False

def is_onap_up():
	cmd="kubectl get pods --field-selector status.phase!=Running -n onap | wc -l"
	result=check_output(cmd, shell=True).decode('utf-8')
	logger.info (f"Checking if ONAP is UP:{result}")
	if int(result) <= 9:
		logger.info ("ONAP is Up")
		return True
	else:
		logger.info ("ONAP is Down")
		return False

def is_nonrtric_up():
	cmd="kubectl get pods --field-selector status.phase!=Running -n nonrtric | wc -l"
	result=check_output(cmd, shell=True).decode('utf-8')
	logger.info (f"Checking if NONRTRIC is UP:{result}")
	if int(result) == 0:
		logger.info ("NONRTRIC is Up")
		return True
	else:
		logger.info ("NONRTRIC is Down")
		return False

def update_event_settings(nfName, nfType):
	file = f'{resources_path}/faults-config/event-settings-'+nfType+'.json'
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

def enable_events_for_all_simulators():
	for container in get_all_simulators():
		name = container.decode("utf-8")
		if "o-" in name:
			if "o-ru" in name:
				print("Set", name, update_event_settings(name, "ru"))
			if "o-du" in name:
				print("Set", name, update_event_settings(name, "du"))


def wait_for_smo_to_be_running():
	wait(lambda: is_onap_up() and is_nonrtric_up(), sleep_seconds=10, timeout_seconds=300, waiting_for="SMO to be ready")

def wait_for_network_simulators_to_be_running():
	wait(lambda: is_network_simulators_up(), sleep_seconds=10, timeout_seconds=60, waiting_for="Network simulators to be ready")

def pytest_sessionstart(session):
	wait_for_smo_to_be_running()
	# Due to an Onap Ves bugs or dmaap ?? DU sims must send messages twice so we need to restart the sims
	start_network_simulators()
	wait_for_network_simulators_to_be_running()
	time.sleep(2)
	dmaap = OranDmaap()
        # Do a first get to register the o1test/o1test user in DMAAP, all messages will then be stored for him
	dmaap.get_message_from_topic("unauthenticated.VES_PNFREG_OUTPUT", 10000, settings.DMAAP_GROUP, settings.DMAAP_USER)

	## Now kill the simulators and restart them for the test session
	stop_network_simulators()

	start_network_simulators()
	wait_for_network_simulators_to_be_running()
	# Wait enough time to have at least the SDNR notifications sent
	logger.info ("Waiting 60s that SDNR sends all registration events to VES")
	time.sleep(60)
	logger.info ("Enabling faults/events reporting on SDNR")
	enable_events_for_all_simulators()

	logger.info ("Test Session setup completed successfully")


def pytest_sessionfinish(session, exitstatus):
	stop_network_simulators()
	logger.info ("Test Session cleanup done")

