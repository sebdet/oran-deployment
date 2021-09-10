#!/bin/bash
kubectl create namespace onap
kubectl create namespace nonrtric
echo '### Installing ONAP part ###'
helm deploy --debug onap local/onap --namespace onap -f ../helm-override/onap-override-cnf.yaml
echo  '### Installing ORAN NONRTRIC part ###'
helm install --debug oran-nonrtric local/nonrtric --namespace nonrtric -f ../helm-override/oran-override.yaml
