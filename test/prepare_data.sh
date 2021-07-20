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

# This script is populating some data into nonrtric for demo/test purpose.
# First this script copies data/ folder into one of the rics, in below case a1-sim-osc-0.
# Then from the ric, run populate_policy_data.sh and populate_enrichment_data.sh.
# populate_policy_data.sh creates policy-types, service, and policies.
# populate_enrichment_data.sh creates EiProducer, EiType, and EiJob.
#
# Why we run the scripts in the ric, not from the host?
# Because a1-simulators(ric) are deployed in statefulset,
# they are not exposed to outside the k8s cluster.
# And we must create policy type into the ric first.
# Similarly, the enrichmentservice is not exposed outside the k8s cluster,
# hence the commands for populating enrichment data need to be run from within the cluster.

kubectl -n nonrtric cp run_in_k8s a1-sim-osc-0:/usr/src/app/
kubectl -n nonrtric exec -it a1-sim-osc-0 -- bash -c 'cd run_in_k8s/ && ./populate_policy_data.sh && ./populate_enrichment_data.sh'
