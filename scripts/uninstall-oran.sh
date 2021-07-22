#!/bin/bash
kubectl delete namespace onap
kubectl delete namespace nonrtric
kubectl delete pv --all
sudo rm -rf /dockerdata-nfs
