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
