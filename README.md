# o-ran-onap-based-smo-deployment

This project investigates how different helm charts from different 
Linux Foundation projects can be integrated into one deployment.

Requirements:
1. A node with Ubuntu server 20.04
2. K8S node setup with Helm 3 and Kubectl + Chartmuseum
	Refer to that wiki page for the setup: https://wiki.onap.org/display/DW/Deploy+OOM+and+SDC+%28or+ONAP%29+on+a+single+VM+with+microk8s+-+Honolulu+Setup

Build the project:
./scripts/build-oran.sh

Install Onap + NonRTRIC:
cd scripts
./install-oran.sh
Note:
Installation can be customized in ./helm-override/onap-override.yaml & ./helm-override/oran-override.yaml

Uninstall:
cd scripts
./uninstall-oran.sh

