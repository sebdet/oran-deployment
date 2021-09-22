#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2020 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================
#

# The scripts in data/ will generate some dummy data in the running system.
# It will create:
# one policy type in a1-sim-OSC
# one service in policy agent
# one policy in a1-sim-OSC
# one policy in a1-sim-STD

# Run command:
# ./prepareDmaapMsg.sh [dmaap-mr host] [a1-sim-OSC host] [a1-sim-STD host] [a1-sim-STD2 host] [http/https]

dmaap_mr_host=${1:-localhost}
a1_sim_OSC_host=${2:-localhost}
a1_sim_STD_host=${3:-localhost}
a1_sim_STD_v2_host=${4:-localhost}
httpx=${5:-"http"}
policy_agent_port=30094
dmaap_mr_port=3904

echo "using dmaap-mr host: "$dmaap_mr_host
echo "using dmaap-mr port: "$dmaap_mr_port
echo "using a1-sim-OSC host: "$a1_sim_OSC_host
echo "using a1-sim-STD host: "$a1_sim_STD_host
echo "using a1-sim-STD-v2 host: "$a1_sim_STD_v2_host
echo "using policy-agent port: "$policy_agent_port
echo "using protocol: "$httpx
echo -e "\n"

echo "dmaap-mr topics: $httpx://$dmaap_mr_host:$dmaap_mr_port/topics/listAll"
curl -skw %{http_code} $httpx://$dmaap_mr_host:$dmaap_mr_port/topics/listAll
echo -e "\n"

echo "dmaap-mr create topic A1-POLICY-AGENT-READ:"
curl -skw %{http_code} -X POST "$httpx://$dmaap_mr_host:$dmaap_mr_port/topics/create" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"topicName\": \"A1-POLICY-AGENT-READ\",  \"topicDescription\": \"test topic\",  \"partitionCount\": 1,  \"replicationCount\": 1,  \"transactionEnabled\": \"false\"}"
echo -e "\n"

echo "dmaap-mr create topic A1-POLICY-AGENT-WRITE:"
curl -skw %{http_code} -X POST "$httpx://$dmaap_mr_host:$dmaap_mr_port/topics/create" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"topicName\": \"A1-POLICY-AGENT-WRITE\",  \"topicDescription\": \"test topic\",  \"partitionCount\": 1,  \"replicationCount\": 1,  \"transactionEnabled\": \"false\"}"
echo -e "\n"

echo "dmaap-mr topics:"
curl -skw %{http_code} $httpx://$dmaap_mr_host:$dmaap_mr_port/topics/listAll
echo -e "\n"

echo "ric1 version:"
curl -skw %{http_code} $httpx://$a1_sim_OSC_host:8085/counter/interface
echo -e "\n"

echo "ric2 version:"
curl -skw %{http_code} $httpx://$a1_sim_STD_host:8085/counter/interface
echo -e "\n"

echo "ric3 version:"
curl -skw %{http_code} $httpx://$a1_sim_STD_v2_host:8085/counter/interface
echo -e "\n"

echo "create policy type 1 to ric1:"
curl -X PUT -skw %{http_code} $httpx://$a1_sim_OSC_host:8085/policytype?id=1 -H Content-Type:application/json --data-binary @testdata/OSC/policy_type.json
echo -e "\n"

echo "create policy type 2 to ric3:"
curl -skw %{http_code} $httpx://$a1_sim_STD_v2_host:8085/policytype?id=2 -X PUT -H Accept:application/json -H Content-Type:application/json -H X-Requested-With:XMLHttpRequest --data-binary @testdata/v2/policy_type.json
echo -e "\n"

for i in {1..60}; do
	echo "policy types from policy agent:"
    curlString="curl -skw %{http_code} $httpx://localhost:$policy_agent_port/policy_types"
    res=$($curlString)
    echo "$res"
    expect="[\"\",\"1\",\"2\"]200"
    if [ "$res" == "$expect" ]; then
        echo -e "\n"
        break;
    else
        sleep $i
    fi
done

## Using PMS v1 interface
echo "create service 1 to policy agent via dmaap_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v1/dmaap-msg-service-create.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

echo "create policies to ric1 & ric2 & ric3 with type1 and service1 via dmaa_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v1/dmaap-msg-policy-create.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

echo "get policy from policy agent via dmaap_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v1/dmaap-msg-policy-get.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

## Using PMS v2 interface
echo "create service 2 to policy agent via dmaap_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v2/dmaap-msg-service-create.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

echo "create policies to ric1 & ric2 & ric3 with type1 and service1 via dmaa_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v2/dmaap-msg-policy-create.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

echo "get policy from policy agent via dmaap_mr:"
curl -k -X POST -sw %{http_code} -H accept:application/json -H Content-Type:application/json "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-READ/" --data-binary @testdata/dmaap/v2/dmaap-msg-policy-get.json
echo -e "\n"

echo "get result from mr of previous request:"
curl -X GET "$httpx://$dmaap_mr_host:$dmaap_mr_port/events/A1-POLICY-AGENT-WRITE/users/policy-agent?timeout=15000&limit=100" -H "accept: application/json" -H "Content-Type: application/json" | jq .
echo -e "\n"

## Get metric from rics
echo "policy numbers from ric1:"
curl -skw %{http_code} $httpx://$a1_sim_OSC_host:8085/counter/num_instances
echo -e "\n"

echo "policy numbers from ric2:"
curl -skw %{http_code} $httpx://$a1_sim_STD_host:8085/counter/num_instances
echo -e "\n"

echo "policy numbers from ric3:"
curl -skw %{http_code} $httpx://$a1_sim_STD_v2_host:8085/counter/num_instances
echo -e "\n"

