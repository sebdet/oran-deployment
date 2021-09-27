#!/bin/bash
kubectl create namespace simulators
echo '### Installing ORAN SIMULATORS part ###'
helm install --debug oran-simulator local/ru-du-simulators --namespace simulators -f $1
