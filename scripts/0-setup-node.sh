#!/bin/bash

echo '### Installing some TOOLS  ###'
apt-get update -y
apt-get upgrade -y
apt-get install -y python3-pip python3.8 maven
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
pip install pipenv

echo '### Installing the K8S cluster using MULTICLOUD KUD INSTALL ###'
../multicloud-k8s/kud/hosting_providers/baremetal/aio.sh

