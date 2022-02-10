#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

# This usecase has limitations due to Clamp issue.
# 1. manually change clamp-be settings before running the test
# 2. make sure using the policy-clamp-be version 6.2.0-snapshot

import time
import subprocess
import logging
import logging.config
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy, PolicyType
from oransdk.policy.clamp import ClampToscaTemplate
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test Control Loops for O-RU Fronthaul Recovery usecase - Apex policy")
dmaap = OranDmaap()
CLAMP_BASICAUTH = { 'username': 'demo@people.osaaf.org', 'password': 'demo123456!' }
clamp = ClampToscaTemplate(CLAMP_BASICAUTH)

policy_id = "onap.policies.native.apex.LinkMonitor"
policy_version = "1.0.0"
policy_type_id = "onap.policies.native.Apex"
policy_type_version = "1.0.0"
policy_type = PolicyType(type=policy_type_id, version=policy_type_version)
engine_name = "LinkMonitorApexEngine"
engine_version = "0.0.1"
engine_id = "101"
deployment_port = "12345"

def update_clamp_config():
    logger.info ("Update the clamp config")
    #cmd="kubectl -n onap get cm onap-policy-clamp-be-configmap -o yaml | sed 's/clamp.config.controlloop.runtime.url=http:/clamp.config.controlloop.runtime.url=https:/' > temp.yaml"
    #check_output(cmd, shell=True).decode('utf-8')
	#cmd="kubectl create configmap onap-policy-clamp-be-configmap -n onap --from-file=temp.yaml -o yaml --dry-run | kubectl apply -f -"
	#check_output(cmd, shell=True).decode('utf-8')
	#cmd="kubectl rollout restart deployment onap-policy-clamp-be -n onap"
	#check_output(cmd, shell=True).decode('utf-8')

def create_topic():
    logger.info("Create new topic")
    topic = '{  "topicName": "unauthenticated.SEC_FAULT_OUTPUT",  "topicDescription": "test topic",  "partitionCount": 1,  "replicationCnCount": 1,  "transactionEnabled": "false"}'
    response = dmaap.create_topic(topic)
    logger.info("response is: %s", response)

def verify_topic_created():
    logger.info("Verify topic created")
    topiclist = dmaap.get_all_topics({})
    topic_created = False
    for topic in topiclist:
      if topic["topicName"] == "unauthenticated.SEC_FAULT_OUTPUT":
          topic_created = True
          break

    if (topic_created):
          logger.info("Topic created successfully")
    else:
          logger.info("Topic creation failed")

def upload_commission(tosca_template):
    logger.info("Upload tosca to commissioning")
    return clamp.upload_commission(tosca_template)

def create_instance(tosca_template):
    logger.info("Create Instance")
    return clamp.create_instance(tosca_template)

def change_instance_status(new_status):
    logger.info("Change Instance Status to %s", new_status)
    try:
        clamp.change_instance_status(new_status, "PMSH_Instance1", "1.2.3")
    except RequestError as exc:
        logger.info("Change Instance Status request returned failed. Will query the instance status to double check whether the request is successful or not.")

    # There's a bug in Clamp code, sometimes it returned 500, but actually the status has been changed successfully
    # Thus we verify the status to determine whether it was successful or not
    time.sleep(2)
    response = clamp.get_template_instance()
    return response["controlLoopList"][0]["orderedState"]

def verify_instance_status(new_status):
    logger.info("Verify the Instance Status is updated to the expected status %s", new_status)
    for x in range(10):
        response = clamp.get_template_instance()
        if response["controlLoopList"][0]["state"] == new_status:
            return True
        else:
            time.sleep(5)

    logger.info("Time out for Status being updated to the expected status", new_status)
    return False

def verify_apex_policy_created():
    logger.info("Verify Apex policy is deployed")
    policy = OranPolicy()
    policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)
    policy_deployed = False
    for status in policy_status_list:
        logger.info("the status %s,%s,%s:", status["policy"]["name"], status["policy"]["version"] , status["deploy"] )
        if (status["policy"]["name"] == "onap.policies.native.apex.LinkMonitor" and status["policy"]["version"] == "1.0.0" and status["deploy"]):
            policy_deployed = True
            break

    if policy_deployed:
        logger.info("Policy deployed successfully")
    else:
        logger.info("Failed to deploy policy")

def delete_template_instance():
    logger.info("Delete Instance")
    return clamp.delete_template_instance("PMSH_Instance1", "1.2.3")

def decommission_tosca():
    logger.info("Decommission tosca")
    return clamp.decommission_template("ToscaServiceTemplateSimple", "1.0.0")

def send_dmaap_event():
    """Send a event to Dmaap that should trigger the apex policy."""
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    dmaap.send_link_failure_event(event)

def test_cl_oru_recovery():
    create_topic()
    verify_topic_created()

    #tosca_template = jinja_env().get_template("ToscaPolicy.json.j2").render(policyId=policy_id, policyVersion=policy_version, policyTypeId=policy_type_id, policyTypeVersion=policy_type_version, engineName=engine_name, engineVersion=engine_version, engineId=engine_id, deploymentPort=deployment_port, dmaapGroup=settings.DMAAP_GROUP, dmaapUser=settings.DMAAP_USER)
    tosca_template = jinja_env().get_template("commission_apex.json.j2").render()

    response = upload_commission(tosca_template)
    assert response["errorDetails"] is None

    response = create_instance(tosca_template)
    assert response["errorDetails"] is None

    response = change_instance_status("PASSIVE")
    assert response == "PASSIVE"
    assert verify_instance_status("PASSIVE")

    response = change_instance_status("RUNNING")
    assert response == "RUNNING"
    assert verify_instance_status("RUNNING")

    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "locked"

    send_dmaap_event()

    verify_apex_policy_created()

    time.sleep(10)
    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "rrm-pol-2", settings.SDNC_BASICAUTH)
    assert status["o-ran-sc-du-hello-world:radio-resource-management-policy-ratio"][0]["administrative-state"] == "unlocked"

    response = change_instance_status("PASSIVE")
    assert response == "PASSIVE"
    assert verify_instance_status("PASSIVE")

    response = change_instance_status("UNINITIALISED")
    assert response == "UNINITIALISED"
    assert verify_instance_status("UNINITIALISED")

    response = delete_template_instance()
    assert response["errorDetails"] is None

    response = decommission_tosca()
    assert response["errorDetails"] is None