#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2022 AT&T Intellectual Property. All rights
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
"""Closed Loop Apex usecase tests module."""
# This usecase has limitations due to Clamp issue.
# 1. make sure using the policy-k8s-participant version is higher than 6.3.0
import logging.config
import subprocess
import os
from subprocess import check_output
import pytest
from waiting import wait
from onapsdk.configuration import settings
from oransdk.utils.jinja import jinja_env
from oransdk.policy.clamp import ClampToscaTemplate
from smo.cl_usecase import ClCommissioningUtils

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

chartmuseum_tls_enabled = True
logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Clamp K8S usecase")
clcommissioning_utils = ClCommissioningUtils()
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)

chartmuseum_url = "http://localhost:8080"
chart_version = "1.0.0"
chart_name = "oru-app"
release_name = "nonrtric"
usecase_name = "k8s_usecase"
resource_folder = f"{dname}/resources/cl-test-helm-chart"

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Prepare the test environment before the executing the tests."""
    logger.info("Test class setup for Closed Loop tests")

    logger.info("Add the remote repo to Clamp k8s pod")
    k8s_pod = subprocess.run("kubectl get pods -n onap | grep k8s | awk '{print $1}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    # Copy helm chart to k8s pod
    logger.info("Copy o-ru helm chart to clamp k8s pod")
    cmd = f"kubectl cp {resource_folder}/oru-app-1.0.0.tgz onap/{k8s_pod}:/home/policy/local-charts/oru-app-1.0.0.tgz"
    check_output(cmd, shell=True).decode('utf-8')

    logger.info("Start chartmuseum on policy k8s pod")
    subprocess.run("curl -LO https://s3.amazonaws.com/chartmuseum/release/latest/bin/linux/amd64/chartmuseum", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    subprocess.run(f"kubectl cp ./chartmuseum onap/{k8s_pod}:/opt/app/policy/clamp/bin/chartmuseum", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    subprocess.run("rm -rf ./chartmuseum", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"chmod +x /opt/app/policy/clamp/bin/chartmuseum\""
    check_output(cmd, shell=True).decode('utf-8')

    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"/opt/app/policy/clamp/bin/chartmuseum --storage local --storage-local-rootdir /home/policy/helm3-storage -port 8080 > /dev/null 2>&1 &\""
    check_output(cmd, shell=True).decode('utf-8')

    logger.info("Deploy o-ru helm chart to clamp k8s pod local repo")
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"curl -k --noproxy '*' -X POST --data-binary @/home/policy/local-charts/oru-app-1.0.0.tgz {chartmuseum_url}/api/charts\""
    check_output(cmd, shell=True).decode('utf-8')

    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm repo add chartmuseum {chartmuseum_url}\""
    check_output(cmd, shell=True).decode('utf-8')
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm repo update\""
    check_output(cmd, shell=True).decode('utf-8')
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm search repo -l oru-app\""
    result = check_output(cmd, shell=True).decode('utf-8')
    if result == '':
        logger.info("Failed to update the K8s pod repo")
    logger.info("Test Session setup completed successfully")

    ### Cleanup code
    yield
    logger.info("Start to cleanup the use case")
    # Finish and delete the cl instance
    clcommissioning_utils.clean_instance(usecase_name)
    wait(lambda: is_oru_app_down(), sleep_seconds=5, timeout_seconds=60, waiting_for="Oru app is down")
    # Remove the remote repo to Clamp k8s pod
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm repo remove chartmuseum\""
    check_output(cmd, shell=True).decode('utf-8')
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"curl -k --noproxy '*' -X DELETE {chartmuseum_url}/api/charts/oru-app/1.0.0\""
    check_output(cmd, shell=True).decode('utf-8')
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"rm -rf /home/policy/local-charts/oru-app-1.0.0.tgz\""
    check_output(cmd, shell=True).decode('utf-8')
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"rm -rf /opt/app/policy/clamp/bin/chartmuseum\""
    check_output(cmd, shell=True).decode('utf-8')
    logger.info("Test Session cleanup done")

def is_chartmuseum_up() -> bool:
    """Check if the chartmuseum is up."""
    cmd = "kubectl get pods --field-selector status.phase=Running -n test"
    result = check_output(cmd, shell=True).decode('utf-8')
    logger.info("Checking if chartmuseum is UP: %s", result)
    if result == '':
        logger.info("chartmuseum is Down")
        return False
    logger.info("chartmuseum is Up")
    return True


def is_oru_app_up() -> bool:
    """Check if the oru-app is up."""
    cmd = "kubectl get pods -n nonrtric | grep oru-app | wc -l"
    result = check_output(cmd, shell=True).decode('utf-8')
    logger.info("Checking if oru-app is up :%s", result)
    if int(result) == 1:
        logger.info("ORU-APP is Up")
        return True
    logger.info("ORU-APP is Down")
    return False

def is_oru_app_down() -> bool:
    """Check if the oru-app is down."""
    cmd = "kubectl get pods -n nonrtric | grep oru-app | wc -l"
    result = check_output(cmd, shell=True).decode('utf-8')
    logger.info("Checking if oru-app is down :%s", result)
    if int(result) == 0:
        logger.info("ORU-APP is Down")
        return True
    logger.info("ORU-APP is Up")
    return False

def test_cl_oru_app_deploy():
    """The Closed Loop O-RU Fronthaul Recovery usecase Apex version."""
    logger.info("Upload tosca to commissioning")
    commissioning_payload = jinja_env().get_template("commission_k8s.json.j2").render(chartmuseumIp="localhost", chartmuseumPort=8080, chartVersion=chart_version, chartName=chart_name, releaseName=release_name)
    instance_payload = jinja_env().get_template("create_instance_k8s.json.j2").render(chartmuseumIp="localhost", chartmuseumPort=8080, chartVersion=chart_version, chartName=chart_name, releaseName=release_name, instanceName=usecase_name)
    assert clcommissioning_utils.create_instance(usecase_name, commissioning_payload, instance_payload) is True

    logger.info("Check if oru-app is up")
    wait(lambda: is_oru_app_up(), sleep_seconds=5, timeout_seconds=300, waiting_for="Oru-app to be up")
