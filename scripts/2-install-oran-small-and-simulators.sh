#!/bin/bash
kubectl create namespace onap
kubectl create namespace nonrtric
kubectl create namespace simulators
echo '### Installing ONAP part ###'
helm deploy --debug onap local/onap --namespace onap -f ../helm-override/onap-override.yaml
echo  '### Installing ORAN NONRTRIC part ###'
helm install --debug oran-nonrtric local/nonrtric --namespace nonrtric -f ../helm-override/oran-override.yaml
echo '### Installing ORAN SIMULATORS part ###'
helm install --debug oran-simulator local/ru-du-simulators --namespace simulators
