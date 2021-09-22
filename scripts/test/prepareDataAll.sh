#!/bin/bash

dmaap_port=3904
ecs_port=9082
a1_sim_port=8085
policy_agent_port=9080
sdnc_port=8282

# get ip of dmaap
echo "Dmaap IP:"
command="kubectl describe pods onap-message-router-0 -n onap | grep IP: | sed -n '2p' | awk  '{print \$2}'"
dmaap_host=$(eval $command)
echo $dmaap_host

# get ip of enrichment service
echo "ECS IP:"
command="kubectl describe pods enrichmentservice-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print \$2}'"
ecs_host=$(eval $command)
echo $ecs_host

# get ip of A1 simulators
echo "OSC IP:"
command="kubectl describe pods a1-sim-osc-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print \$2}'"
a1_osc_host=$(eval $command)
echo $a1_osc_host

echo "STD IP:"
command="kubectl describe pods a1-sim-std-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print \$2}'"
a1_std_host=$(eval $command)
echo $a1_std_host

echo "STD2 IP:"
command="kubectl describe pods a1-sim-std2-0 -n nonrtric | grep IP: | sed -n '2p' | awk  '{print \$2}'"
a1_std2_host=$(eval $command)
echo $a1_std2_host

echo "Policy Agent IP:"
command="kubectl describe pods policymanagementservice-0 -n nonrtric | grep IP | sed -n '2p' | awk  '{print \$2}'"
policy_agent_host=$(eval $command)
echo $sdnc_host

echo "A1 Controller IP:"
command="kubectl describe service a1controller -n nonrtric | grep IP | sed -n '2p' | awk  '{print \$2}'"
sdnc_host=$(eval $command)
echo $sdnc_host

dmaap_url=$dmaap_host:$dmaap_port
a1_osc_url=$a1_osc_host:$a1_sim_port
a1_std_url=$a1_std_host:$a1_sim_port
a1_std2_url=$a1_std2_host:$a1_sim_port
policy_agent_url=$policy_agent_host:$policy_agent_port
sdnc_url=$sdnc_host:$sdnc_host
esc_url=$ecs_host:$ecs_port

./health_check.sh $ecs_host $a1_osc_url $a1_std_url $a1_std2_url $policy_agent_url $sdnc_url
cd ./data
./prepareDmaapMsg.sh $dmaap_url $a1_osc_url $a1_std_url $a1_std2_url $policy_agent_url
./preparePmsData.sh $a1_osc_url $a1_std2_url $policy_agent_url
./prepareEcsData.sh $esc_url
