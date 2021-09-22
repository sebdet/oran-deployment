#!/usr/bin/env bash

enrichment_service_host=${1:-localhost}
a1_sim_OSC_host=${2:-localhost}
a1_sim_STD_host=${3:-localhost}
a1_sim_STD_v2_host=${4:-localhost}

echo -e "\n"
echo "using enrichment service host: "$enrichment_service_host
echo "using a1-sim-OSC host: "$a1_sim_OSC_host
echo "using a1-sim-STD host: "$a1_sim_STD_host
echo "using a1-sim-STD-v2 host: "$a1_sim_STD_v2_host

echo -e "\n"

checkStatus(){
    for i in {1..60}; do
        res=$($1)
        echo "$res"
        expect=$2
        if [ "$res" == "$expect" ]; then
            echo -e "$3 is alive!\n"
            break;
        else
            sleep $i
        fi
    done
}

# check SIM1 status
echo "check SIM1 status:"
checkStatus "curl -skw %{http_code} http://$a1_sim_OSC_host:8085/" "OK200" "SIM1"

# check SIM2 status
echo "check SIM2 status:"
checkStatus "curl -skw %{http_code} http://$a1_sim_STD_host:8085/" "OK200" "SIM2"

# check SIM3 status
echo "check SIM3 status:"
checkStatus "curl -skw %{http_code} http://$a1_sim_STD_v2_host:8085/" "OK200" "SIM3"

# check PMS status
echo "check PMS status:"
checkStatus "curl -skw %{http_code} http://localhost:30094/status" "hunky dory200" "PMS"

# check ECS status
echo "check ECS status:"
checkStatus "curl -skw %{http_code} http://$enrichment_service_host:8083/status" '{"status":"hunky dory","no_of_producers":0,"no_of_types":0,"no_of_jobs":0}200' "ECS"

echo "NONRTRIC health check passed."
