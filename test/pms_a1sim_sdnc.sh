#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
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


enrichment_service_host=${1:-localhost}
a1_sim_OSC_host=${2:-localhost}
a1_sim_STD_host=${3:-localhost}
a1_sim_STD_v2_host=${4:-localhost}
a1_controller_url=${5:-localhost:8282}

echo -e "\n"
echo "using enrichment service host: "$enrichment_service_host
echo "using a1-sim-OSC host: "$a1_sim_OSC_host
echo "using a1-sim-STD host: "$a1_sim_STD_host
echo "using a1-sim-STD-v2 host: "$a1_sim_STD_v2_host
echo "using a1 controller url: "$a1_controller_url
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

# check SDNC status
echo "check SDNC status:"
checkStatus "curl -s -o /dev/null -I -w %{http_code} http://$a1_controller_url/apidoc/explorer/" "200" "SDNC"

cd ./data
./preparePmsData.sh $a1_sim_OSC_host $a1_sim_STD_v2_host
./prepareEcsData.sh $enrichment_service_host
