#!/bin/bash
kubectl create namespace onap
echo '### Installing ONAP part###'
helm deploy --debug onap local/onap --namespace onap -f oran-override.yaml
echo  '### Installing ORAN part ###'
helm install --debug oran local/oran --namespace onap -f oran-override.yaml
