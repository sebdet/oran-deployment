#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import time
import subprocess
import logging
import logging.config
from onapsdk.configuration import settings
from oransdk.dmaap.dmaap import OranDmaap
from oransdk.policy.policy import OranPolicy, PolicyType
from oransdk.sdnc.sdnc import OranSdnc
from oransdk.utils.jinja import jinja_env

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("test APEX policy")

def test_a1():
    dmaap = OranDmaap()
    logger.info("Create new topic")
    topic = '{  "topicName": "unauthenticated.SEC_FAULT_OUTPUT",  "topicDescription": "test topic",  "partitionCount": 1,  "replicationCnCount": 1,  "transactionEnabled": "false"}'
    response = dmaap.create_topic(topic)
    logger.info("response is: %s", response)

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


    logger.info("Verify policy components are ready")
    policy = OranPolicy()
    policy_ready = {"api_ready": False, "pap_ready": False, "apex_ready": False}
    for x in range(60):
        policy_status = policy.get_components_status(settings.POLICY_BASICAUTH)
        if (policy_status["api"]["healthy"] and policy_ready["api_ready"] == False):
            logger.info("Policy Api is ready")
            policy_ready["api_ready"] = True
        if (policy_status["pap"]["healthy"] and policy_ready["pap_ready"] == False):
            logger.info("Policy Pap is ready")
            policy_ready["pap_ready"] = True
        if (policy_status["pdps"]["apex"][0]["healthy"] == "HEALTHY" and policy_ready["apex_ready"] == False):
            logger.info("Policy Apex is ready")
            policy_ready["apex_ready"] = True
        if (policy_ready["api_ready"] and policy_ready["pap_ready"] and policy_ready["apex_ready"]):
            logger.info("Policy status all ready")
            break


    if (policy_ready["api_ready"] == False or policy_ready["pap_ready"] == False or policy_ready["apex_ready"] == False):
        logger.info("Policy components are not ready. Exit the test.")


    logger.info("Create policy")
    policy_data = jinja_env().get_template("ToscaPolicy.json.j2").render()
    policy.create_policy(PolicyType(type="onap.policies.native.Apex", version="1.0.0"), policy_data, settings.POLICY_BASICAUTH)

    logger.info("Verify whether policy created successfully")
    policy_response = policy.get_policy(PolicyType(type="onap.policies.native.Apex", version="1.0.0"),
                                        "onap.policies.native.apex.LinkMonitor", "1.0.0", settings.POLICY_BASICAUTH)
    if (policy_response):
        logger.info("Policy created successfully")
    else:
        logger.info("Policy creation failed")

    logger.info("Deploy policy")
    deploy_policy = jinja_env().get_template("DeployPolicyPAP.json.j2").render()
    policy.deploy_policy(deploy_policy, settings.POLICY_BASICAUTH)

    logger.info("Verify the policy is deployed")
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

    logger.info("Check O-du/O-ru status")
    SDNC_BASICAUTH = { 'username': 'admin', 'password': 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U' }
    sdnc = OranSdnc()
    status = sdnc.get_odu_oru_status("o-du-1122", "o-ru-11221", SDNC_BASICAUTH)
    if status["o-ran-sc-du-hello-world:du-to-ru-connection"][0]["administrative-state"] == "LOCKED":
        logger.info("The initial state of o-du o-ru connection is LOCKED")

    logger.info("Wait for a while for Apex engine to be ready before sending Dmaap event")
    dmaap = OranDmaap()
    event = jinja_env().get_template("LinkFailureEvent.json.j2").render()
    for x in range(60):
        dmaap.send_link_failure_event(event)
        output = subprocess.getoutput('kubectl logs onap-policy-apex-pdp-0 -n onap | grep "Task Selection Execution: \'LinkMonitorPolicy:0.0.1:NULL:LinkFailureOrClearedState\'" | wc -l')
        if (int(output) > 0):
            logger.info("Apex engine is ready. LinkFailureEvent sent to Dmaap")
            break
        else:
            logger.info("Apex engine not ready yet, wait for a while and try again")
            time.sleep(2)

    logger.info("Check O-du/O-ru status again")
    status = sdnc.get_odu_oru_status("o-du-1122", "o-ru-11221", SDNC_BASICAUTH)
    if status["o-ran-sc-du-hello-world:du-to-ru-connection"][0]["administrative-state"] == "UNLOCKED":
        logger.info("The updated state of o-du o-ru connection is UNLOCKED")
