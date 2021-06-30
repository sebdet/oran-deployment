#!/bin/bash
kubectl create namespace nonrtric
echo '### Installing ONAP part###'
helm deploy --debug onap local/onap --namespace nonrtric -f oran-override.yaml
echo  '### Installing ORAN part ###'
helm install --debug oran local/oran --namespace nonrtric -f oran-override.yaml
