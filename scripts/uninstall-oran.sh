#!/bin/bash
kubectl delete namespace onap
kubectl delete namespace nonrtric
kubectl delete namespace simulators
kubectl delete pv --all
sudo rm -rf /dockerdata-nfs
