#!/bin/bash
kubectl create namespace nonrtric
echo  '### Installing ORAN NONRTRIC part ###'
helm install --debug oran-nonrtric local/nonrtric --namespace nonrtric -f $1
