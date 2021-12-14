import pytest
from subprocess import check_output
from waiting import wait
import os

resources_path="./resources"

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def start_network_simulators():
	cmd="kubectl create namespace network"
	check_output(cmd, shell=True).decode('utf-8')
	cmd=f"helm install --debug oran-simulator local/ru-du-simulators --namespace network -f {resources_path}/network-simulators-override.yaml -f {resources_path}/network-simulators-topology-override.yaml"
	check_output(cmd, shell=True).decode('utf-8')

def stop_network_simulators():
        cmd="kubectl delete namespace network"
        return check_output(cmd, shell=True).decode('utf-8')

def is_network_simulators_up():
	cmd="kubectl get pods --field-selector status.phase!=Running -n network"
	result=check_output(cmd, shell=True).decode('utf-8')
	print (f"Check:{result}")
	if "" == result:
		print ("Up")
		return True
	else:
		print ("Down")
		return False

def wait_for_network_simulators_to_be_running():
	wait(lambda: is_network_simulators_up(), sleep_seconds=5, timeout_seconds=60, waiting_for="Network simulators to be ready")

#@pytest.fixture(scope="session")
def pytest_sessionstart(session):
	# Due to a Onap Ves bugs or dmaap ?? DU sims must send messages twice
	start_network_simulators()
	wait_for_network_simulators_to_be_running()
	stop_network_simulators()
	start_network_simulators()
	wait_for_network_simulators_to_be_running()

def pytest_sessionfinish(session, exitstatus):
	stop_network_simulators()
