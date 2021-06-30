#!/bin/bash
kubectl delete namespace nonrtric
kubectl delete pv --all
sudo rm -rf /dockerdata-nfs
