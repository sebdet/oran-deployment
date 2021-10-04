#!/bin/bash
set +x

if ! [ -x "$(command -v jq)" ]; then
  echo 'Error: jq is not installed. Try to install it with APT-GET, YUM or APK' >&2
  echo 'e.g:    sudo apt-get update && apt-get -y install jq'

  exit 1
fi


dmaap_port=3904
ecs_port=8083
a1_sim_port=8085
policy_agent_port=8081
sdnc_port=8282

# get ip of dmaap
dmaap_url=`kubectl get services message-router -n onap |grep message-router | awk '{print $3}'`:$dmaap_port
echo "Dmaap Address:" $dmaap_url

# get ip of enrichment service
ecs_url=`kubectl get services enrichmentservice -n nonrtric | grep enrichmentservice | awk '{print $3}'`:$ecs_port
echo "Enrichment Service Address:" $ecs_url

# get ip of A1 simulators
a1_osc_url=`kubectl describe pods a1-sim-osc-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print $2}'`:$a1_sim_port
echo "A1 SIM OSC Address 0:" $a1_osc_url

a1_std_url=`kubectl describe pods a1-sim-std-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print $2}'`:$a1_sim_port
echo "A1 SIM STD Address 0:" $a1_std_url

a1_std2_url=`kubectl describe pods a1-sim-std2-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print $2}'`:$a1_sim_port
echo "A1 SIM STD Address 2:" $a1_std2_url

policy_agent_url=`kubectl get service policymanagementservice -n nonrtric | grep policymanagementservice | awk  '{print $3}'`:$policy_agent_port
echo "Policy Agent IP:" $policy_agent_url

sdnc_url=`kubectl get service a1controller -n nonrtric | grep a1controller  | awk  '{print $3}'`:$sdnc_port
echo "A1 Controller IP:" $sdnc_url

./health_check.sh $ecs_url $a1_osc_url $a1_std_url $a1_std2_url $policy_agent_url $sdnc_url
cd ./data
./prepareDmaapMsg.sh $dmaap_url $a1_osc_url $a1_std_url $a1_std2_url $policy_agent_url
./preparePmsData.sh $a1_osc_url $a1_std2_url $policy_agent_url
./prepareEcsData.sh $ecs_url
