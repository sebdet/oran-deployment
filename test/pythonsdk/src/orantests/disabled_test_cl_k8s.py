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
# 1. make sure using the policy-clamp-be version 6.2.0-snapshot-latest at this the moment

import time
import logging
import logging.config
import pytest
import subprocess
import os
from waiting import wait
from onapsdk.configuration import settings
from onapsdk.exceptions import RequestError
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env
from subprocess import check_output, run

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Apex policy")
dmaap = OranDmaap()
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)

@pytest.fixture(scope="module", autouse=True)
def setup_simulators():
    """Prepare the test environment before the executing the tests."""
    logger.info("Test class setup for Closed Loop tests")

    # Stop ORU App pod
    logger.info("Disable Oru-app")
    resources_path = "./resources/cl-test-oran-overrides"
    cmd = f"helm upgrade --debug oran-nonrtric local/nonrtric --namespace nonrtric -f {resources_path}/oran-override-disable-oru-app.yaml"
    check_output(cmd, shell=True).decode('utf-8')

    wait(lambda: is_oru_app_disabled(), sleep_seconds=10, timeout_seconds=60, waiting_for="Oru-app is disabled")

    # Add the remote repo to Clamp k8s pod
    logger.info("Add the remote repo to Clamp k8s pod")
    k8s_pod = subprocess.run("kubectl get pods -n onap | grep k8s | awk '{print $1}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    repo_host = subprocess.run("hostname -I | awk '{print $1}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    repo_port = 8080
    logger.info("k8s: %s, repo_host:%s", k8s_pod, repo_host)
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm repo add chartmuseum http://{repo_host}:{repo_port}\""
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
    logger.info("Restart Oru-app")
    cmd = f"helm upgrade --debug oran-nonrtric local/nonrtric --namespace nonrtric -f {resources_path}/oran-override.yaml"
    check_output(cmd, shell=True).decode('utf-8')
    wait(lambda: is_oru_app_enabled(), sleep_seconds=10, timeout_seconds=60, waiting_for="Oru-app is restarted")

    # Remove the remote repo to Clamp k8s pod
    cmd = f"kubectl exec -it -n onap {k8s_pod} -- sh -c \"helm repo remove chartmuseum\""
    check_output(cmd, shell=True).decode('utf-8')
    logger.info("Test Session cleanup done")

def is_oru_app_disabled() -> bool:
    """Check if the oru-app is stopped."""
    result = check_output("kubectl get pods -n nonrtric | grep oru-app | wc -l", shell=True)
    logger.info("Checking if oru-app is stopped: %s", result)
    if result == b'0\n':
        logger.info("oru-app is stopped")
        return True
    logger.info("oru-app is still running")
    return False

def is_oru_app_enabled() -> bool:
    """Check if the oru-app is restarted."""
    cmd = "kubectl get pods --field-selector status.phase=Running -n nonrtric | grep oru-app | wc -l"
    result = check_output(cmd, shell=True)
    logger.info("Checking if oru-app is restarted: %s", result)
    if result == b'1\n':
        logger.info("oru-app is running")
        return True
    logger.info("oru-app is not running")
    return False

def add_remote_repo():
    """Config the clamp k8s pod."""
    logger.info("Add remote repo to the clamp k8s pod")
    pod_name="onap-policy-clamp-cl-k8s-ppnt-6ddb58cfbd-2m8kn"
    ip="135.41.21.24"
    cmd=f"kubectl exec -it -n onap {pod_name} -- sh -c \"helm repo add chartmuseum {ip}:8080\""
    cmd=f"kubectl exec -it -n onap {pod_name} -- sh -c \"helm repo update\""
    check_output(cmd, shell=True).decode('utf-8')


def test_cl_oru_recovery():
    """The Closed Loop O-RU Fronthaul Recovery usecase Apex version."""

