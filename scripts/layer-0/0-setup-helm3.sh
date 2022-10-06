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

#Helm package
wget https://get.helm.sh/helm-v3.5.4-linux-amd64.tar.gz
mv helm-v3.5.4-linux-amd64.tar.gz /tmp/helm-v3.5.4-linux-amd64.tar.gz
cd /tmp/
tar xvfz /tmp/helm-v3.5.4-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/helm
apt-get install git -y

SCRIPT=$(readlink -f "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
cd $SCRIPT_PATH

echo "Checking HELM ..."
helm version
plugin_path=$(helm env | grep HELM_PLUGINS | cut -d'"' -f2)
echo "plugin path is: $plugin_path"
cp ../packages/helm.tar $plugin_path
tar xvfz $plutin_path/helm.tar
res=$(ls -lrt $plugin_path)
echo "list plugin folder: $res"
rm -rf $plugin_path/helm.tar
res=$(ls -lrt $plugin_path)
echo "list plugin folder: $res"
res=$(helm plugin list)
echo "list plugins: $res"
helm repo remove local
helm repo add local http://localhost:18080
