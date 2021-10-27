#!/usr/bin/env bash

enrichment_service_url=${1:-localhost:9082}
a1_sim_OSC_url=${2:-localhost:8085}
a1_sim_STD_url=${3:-localhost:8085}
a1_sim_STD_v2_url=${4:-localhost:8085}
policy_agent_url=${5:-localhost:9080}
a1_controller_url=${6:false}

echo -e "NONRTRIC HealthCheck\n"
echo "using enrichment service url: "$enrichment_service_url
echo "using a1-sim-OSC url: "$a1_sim_OSC_url
echo "using a1-sim-STD url: "$a1_sim_STD_url
echo "using a1-sim-STD-v2 url: "$a1_sim_STD_v2_url
echo "using policy agent url: "$policy_agent_url
if [ "$a1_controller_url" != "false" ]; then
  echo "using a1 controller url: "$a1_controller_url
fi

echo -e "\n"

checkStatus(){
    for i in {1..60}; do
        res=$($1)
        echo "$res"
        expect=$2
        if [[ $res == *"$expect"* ]]; then
            echo -e "$3 is alive!\n"
            break;
        else
            sleep $i
        fi
    done
}

# check SIM1 status
echo "check SIM1(OSC) status:"
checkStatus "curl -vskw %{http_code} http://$a1_sim_OSC_url/" "OK200" "SIM1"

# check SIM2 status
echo "check SIM2(STD) status:"
checkStatus "curl -vskw %{http_code} http://$a1_sim_STD_url/" "OK200" "SIM2"

# check SIM3 status
echo "check SIM3(STD) status:"
checkStatus "curl -vskw %{http_code} http://$a1_sim_STD_v2_url/" "OK200" "SIM3"

# check PMS status
echo "check Policy Agent status:"
checkStatus "curl -vskw %{http_code} http://$policy_agent_url/status" "hunky dory200" "PMS"

# check ECS status
echo "check Enrichment service status:"
checkStatus "curl -vskw %{http_code} http://$enrichment_service_url/status" '{"status":"hunky dory"' "ECS"

if [ "$a1_controller_url" != "false" ]; then
  # check SDNC status
  echo "check A1 Controller (SDNC) status:"
  checkStatus "curl -s -o /dev/null -I -w %{http_code} http://$a1_controller_url/apidoc/explorer/" "200" "SDNC"
fi



echo "NONRTRIC health check passed."
