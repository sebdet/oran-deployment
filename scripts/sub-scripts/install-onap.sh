#!/bin/bash
kubectl create namespace onap
echo '### Installing ONAP part ###'
helm deploy --debug onap local/onap --namespace onap -f $1
