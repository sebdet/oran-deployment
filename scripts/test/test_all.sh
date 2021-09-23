#!/bin/bash

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

echo "A1 Controller IP:"
command="kubectl describe service a1controller -n nonrtric | grep IP | sed -n '2p' | awk  '{print \$2}'"
sdnc_host=$(eval $command)
echo $sdnc_host

cd ./data
./prepareDmaapMsg.sh $dmaap_host $a1_osc_host $a1_std_host $a1_std2_host

cd ..
./pms_a1sim_sdnc.sh $ecs_host $a1_osc_host $a1_std_host $a1_std2_host $sdnc_host:8282