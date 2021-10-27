#!/bin/bash

###
# ============LICENSE_START=======================================================
# ORAN SMO Package
# ================================================================================
# Copyright (C) 2021 AT&T Intellectual Property. All rights
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
pap_port=6969
api_port=6969
dmaap_port=3904
sdnc_port=8282

pap_url=`kubectl get services policy-pap -n onap |grep policy-pap | awk '{print $3}'`:$pap_port
echo "Policy pap url: $pap_url"

api_url=`kubectl get services policy-api -n onap |grep policy-api | awk '{print $3}'`:$api_port
echo "Policy api url: $api_url"

dmaap_url=`kubectl get services message-router -n onap |grep message-router | awk '{print $3}'`:$dmaap_port
echo "Dmaap url: $dmaap_url"

sdnc_url=`kubectl get services -n onap | grep sdnc-oam | awk  '{print $3}'`:$sdnc_port
echo "SDNC url: $sdnc_url"
echo -e "\n"

verifyApexPolicyStatus(){
    for i in {1..60}; do
        curl  -s -o /dev/null -X POST -H accept:application/json -H Content-Type:application/json "http://$dmaap_url/events/unauthenticated.SEC_FAULT_OUTPUT/" -d @./data/LinkFailureEvent.json
        sleep 3
        res=`kubectl logs onap-policy-apex-pdp-0 -n onap | grep "Task Selection Execution: 'LinkMonitorPolicy:0.0.1:NULL:LinkFailureOrClearedState'" | wc -l`
        if [[ $res != 0 ]]; then
            echo -e "LinkFailureEvent sent to Dmaap\n"
            break;
        else
            sleep 2
        fi
    done
}

checkStatus(){
        echo "res:$1"
        if [ "$1" == "$2" ]; then
            echo -e "$3\n"
        else
            echo -e "Result is not as expected: $2\n"
            exit;
        fi
}

checkPolicyStatus(){
    for i in {1..60}; do
        res=$(curl -sk -u 'healthcheck:zb!XztG34' -X GET "https://$pap_url/policy/pap/v1/components/healthcheck")
        apex_info=$(echo $res| cut -d'{' -f 4)

        echo "Verify policy Pap"
        if [[ $res == *"url\":\"https://$1:6969/policy/pap/v1/healthcheck\",\"healthy\":true"* ]]; then
          echo "Policy Pap is ready"
          echo "Verify policy api"
          if [[ $res == *"url\":\"https://$2:6969/policy/api/v1/healthcheck\",\"healthy\":true"* ]]; then
            echo "Policy API is ready"
            echo "Verify policy Apex pdp"
            if [[ $apex_info == *"instanceId\":\"apex"*  && $apex_info == *"healthy\":\"HEALTHY"* ]]; then
              echo "Policy APEX pdp is ready"
              break;
            else
              echo "Policy Apex pdp not ready yet. Wait for a while and retry."
              sleep $i
            fi
          else
            echo "Policy api not ready yet. Wait for a while and retry."
            sleep $i
          fi
        else
          echo "Policy Pap not ready yet. Wait for a while and retry."
          sleep $i
        fi
    done
}

checkPolicyDeployment (){
  res=$(curl -sk -u 'healthcheck:zb!XztG34' -X GET "https://$pap_url/policy/pap/v1/policies/status")
  str1="onap.policies.native.apex.LinkMonitor\",\"version\":\"1.0.0\"},\"policyType\":{\"name\":\"onap.policies.native.Apex\",\"version\":\"1.0.0\"},\"deploy\":true"
        if [[ $res == *"$str1"* ]]; then
          echo "Policy successfully deployed"
        else
          echo "Policy deployment failed"
          exit;
        fi
}

echo "Create topic:"
curl -sk -X POST "http://$dmaap_url/topics/create" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"topicName\": \"unauthenticated.SEC_FAULT_OUTPUT\",  \"topicDescription\": \"test topic\",  \"partitionCount\": 1,  \"replicationCnCount\": 1,  \"transactionEnabled\": \"false\"}"
echo "Get topics:"
curl -sk http://$dmaap_url/topics/listAll
echo -e "\n"

echo "Policy component healthcheck:"
pap_pod=`kubectl get pods -n onap | grep onap-policy-pap | awk  '{print $1}'`
api_pod=`kubectl get pods -n onap | grep onap-policy-api | awk  '{print $1}'`
checkPolicyStatus $pap_pod $api_pod
echo -e "\n"

echo "Create policy:"
res=`curl -sk -u 'healthcheck:zb!XztG34' -X POST "https://$api_url/policy/api/v1/policytypes/onap.policies.native.Apex/versions/1.0.0/policies" -H "Accept: application/json" -H "Content-Type: application/json" -d @./data/ToscaPolicy.json`
res2=`curl -sk -u 'healthcheck:zb!XztG34' -X GET "https://$api_url/policy/api/v1/policytypes/onap.policies.native.Apex/versions/1.0.0/policies/onap.policies.native.apex.LinkMonitor/versions/1.0.0"`
if [[ $res2 ]]; then
    echo "Policy created successfully"
fi
echo -e "\n"

echo "Deploy the policy to apex-pdp via Policy PAP:"
curl -sk -u 'healthcheck:zb!XztG34' -X POST "https://$pap_url/policy/pap/v1/pdps/policies" -H "Accept: application/json" -H "Content-Type: application/json" -d @./data/DeployPolicyPAP.json
echo -e "\n"

echo "Verify policy deployed:"
checkPolicyDeployment
echo -e "\n"

echo "Check O-du/O-ru status"
res=$(curl -sk -H "Authorization: Basic YWRtaW46S3A4Yko0U1hzek0wV1hsaGFrM2VIbGNzZTJnQXc4NHZhb0dHbUp2VXkyVQ==" -X GET "http://$sdnc_url/rests/data/network-topology:network-topology/topology=topology-netconf/node=o-du-1122/yang-ext:mount/o-ran-sc-du-hello-world:network-function/du-to-ru-connection=o-ru-11221")
expected="{\"o-ran-sc-du-hello-world:du-to-ru-connection\":[{\"name\":\"o-ru-11221\",\"operational-state\":\"ENABLED\",\"administrative-state\":\"LOCKED\",\"status\":\"disconnected\"}]}"
checkStatus $res $expected "O-ru has status LOCKED"

echo -e "\n"
echo "Wait for a while for Apex engine to be ready before sending Dmaap event"
verifyApexPolicyStatus

echo -e "\n"
echo "Wait for a while and check O-du/O-ru status again"
sleep 5
res=$(curl -sk -H "Authorization: Basic YWRtaW46S3A4Yko0U1hzek0wV1hsaGFrM2VIbGNzZTJnQXc4NHZhb0dHbUp2VXkyVQ==" -X GET "http://$sdnc_url/rests/data/network-topology:network-topology/topology=topology-netconf/node=o-du-1122/yang-ext:mount/o-ran-sc-du-hello-world:network-function/du-to-ru-connection=o-ru-11221")
expected="{\"o-ran-sc-du-hello-world:du-to-ru-connection\":[{\"name\":\"o-ru-11221\",\"operational-state\":\"ENABLED\",\"administrative-state\":\"UNLOCKED\",\"status\":\"disconnected\"}]}"
checkStatus $res $expected "O-ru has status UNLOCKED"

