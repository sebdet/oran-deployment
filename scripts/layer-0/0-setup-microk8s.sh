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

## Microk8S part
sudo apt-get update
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
snap remove microk8s
snap remove kubectl
snap install microk8s --classic --channel=1.22/stable
sudo snap install kubectl --classic --channel=1.22/stable

## Firewall
ufw allow in on cni0 && sudo ufw allow out on cni0
ufw default allow routed

## Enable required features for K8S
microk8s enable dns storage prometheus

## Setup kubectl
cd
mkdir -p .kube
cd .kube
sudo microk8s.config > config
chmod 700 config

#Check the install
echo "Checking Kubernetes ..."
kubectl version
