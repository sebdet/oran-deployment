#!/bin/bash
kubectl create namespace network
echo '### Installing ORAN SIMULATORS part ###'
helm install --debug oran-simulator local/ru-du-simulators --namespace network -f $1
