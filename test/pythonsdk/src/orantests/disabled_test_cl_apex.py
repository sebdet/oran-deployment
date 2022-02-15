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
# 1. manually change clamp-be settings before running the test:
#    - run command "kubectl -n onap edit cm onap-policy-clamp-be-configmap"
#      find variable clamp.config.controlloop.runtime.url and change http into https
#    - run command "kubectl rollout restart deployment onap-policy-clamp-be -n onap"
#      and wait until policy-clamp-be pod restarted successfully
# 2. make sure using the policy-clamp-be version 6.2.0-snapshot-latest at this the moment

import time
import logging
import logging.config
from onapsdk.configuration import settings
from onapsdk.exceptions import RequestError
from waiting import wait
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Apex policy")
dmaap = OranDmaap()
clamp = ClampToscaTemplate(settings.CLAMP_BASICAUTH)

def create_topic():
    """Create the topic in Dmaap."""
    logger.info("Create new topic")
    topic = '{  "topicName": "unauthenticated.SEC_FAULT_OUTPUT",  "topicDescription": "test topic",  "partitionCount": 1,  "replicationCnCount": 1,  "transactionEnabled": "false"}'
    response = dmaap.create_topic(topic)
    logger.info("response is: %s", response)

def verify_topic_created():
    """Verify whether needed topic created."""
    logger.info("Verify topic created")
    topiclist = dmaap.get_all_topics({})
    topic_created = False
    for topic in topiclist:
        if topic["topicName"] == "unauthenticated.SEC_FAULT_OUTPUT":
            topic_created = True
            break

    if topic_created:
        logger.info("Topic created successfully")
    else:
        logger.info("Topic creation failed")

def upload_commission(tosca_template):
    """
    Upload the tosca to commissioning.

    Args:
        tosca_template : the tosca template to upload in json format
    Returns:
        the response from the upload action
    """
    logger.info("Upload tosca to commissioning")
    return clamp.upload_commission(tosca_template)

def create_instance(tosca_template):
    """
    Create a instance.

        Args:
            tosca_template : the tosca template to create in json format
        Returns:
            the response from the creation action
    """
    logger.info("Create Instance")
    return clamp.create_instance(tosca_template)

def change_instance_status(new_status) -> str:
    """
    Change the instance statue.

    Args:
        new_status : the new instance to be changed to
    Returns:
        the new status to be changed to
    """
    logger.info("Change Instance Status to %s", new_status)
    try:
        clamp.change_instance_status(new_status, "PMSH_Instance1", "1.2.3")
    except RequestError:
        logger.info("Change Instance Status request returned failed. Will query the instance status to double check whether the request is successful or not.")

    # There's a bug in Clamp code, sometimes it returned 500, but actually the status has been changed successfully
    # Thus we verify the status to determine whether it was successful or not
    time.sleep(2)
    response = clamp.get_template_instance()
    return response["controlLoopList"][0]["orderedState"]

def verify_instance_status(new_status):
    """
    Verify whether the instance changed to the new status.

    Args:
        new_status : the new status of the instance
    Returns:
        the boolean value indicating whether status changed successfully
    """
    logger.info("Verify the Instance Status is updated to the expected status %s", new_status)
    response = clamp.get_template_instance()
    if response["controlLoopList"][0]["state"] == new_status:
        return True
    return False

def verify_apex_policy_created():
    """
    Verify whether the Apex policy has deployed successfully.

    Returns:
        the boolean value indicating whether policy deployed successfully
    """
    logger.info("Verify Apex policy is deployed")
    policy = OranPolicy()
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)

    for status in policy_status_list:
        logger.info("the status %s,%s,%s:", status["policy"]["name"], status["policy"]["version"], status["deploy"])
        if (status["policy"]["name"] == "operational.apex.linkmonitor" and status["policy"]["version"] == "1.0.0" and status["deploy"]):
            return True

    logger.info("Failed to deploy Apex policy")
    return False

def delete_template_instance():
    """
    Delete the template instance.

    Returns:
        the response from the deletion action
    """
    logger.info("Delete Instance")
    return clamp.delete_template_instance("PMSH_Instance1", "1.2.3")

def decommission_tosca():
    """
    Decommission the tosca template.

    Returns:
        the response from the decommission action
    """
    logger.info("Decommission tosca")
    return clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")

def send_dmaap_event():
    """Send a event to Dmaap that should trigger the apex policy."""
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    dmaap.send_link_failure_event(event)

def test_cl_oru_recovery():
    """The Closed Loop O-RU Fronthaul Recovery usecase Apex version."""
    create_topic()
    verify_topic_created()

    tosca_template = jinja_env().get_template("commission_apex.json.j2").render()

    response = upload_commission(tosca_template)
    assert response["errorDetails"] is None

    response = create_instance(tosca_template)
    assert response["errorDetails"] is None

    response = change_instance_status("PASSIVE")
    assert response == "PASSIVE"
    wait(lambda: verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to PASSIVE")

    response = change_instance_status("RUNNING")
    assert response == "RUNNING"
    wait(lambda: verify_instance_status("RUNNING"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to RUNNING")

    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"

    send_dmaap_event()

    assert verify_apex_policy_created()

    time.sleep(20)
    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"

    response = change_instance_status("PASSIVE")
    assert response == "PASSIVE"
    wait(lambda: verify_instance_status("PASSIVE"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to PASSIVE")

    response = change_instance_status("UNINITIALISED")
    assert response == "UNINITIALISED"
    wait(lambda: verify_instance_status("UNINITIALISED"), sleep_seconds=5, timeout_seconds=60, waiting_for="Clamp instance switches to UNINITIALISED")

    response = delete_template_instance()
    assert response["errorDetails"] is None

    response = decommission_tosca()
    assert response["errorDetails"] is None
