# o-ran-onap-based-smo-deployment

This project investigates how different helm charts from different 
Linux Foundation projects can be integrated into one deployment.

Requirements:
* K8S node setup with Helm 3 and Kubectl + Chartmuseum, multiple options are available:
	- Wiki that can help to setup it: https://wiki.onap.org/display/DW/Deploy+OOM+and+SDC+%28or+ONAP%29+on+a+single+VM+with+microk8s+-+Honolulu+Setup
  	- Use scripts/0-setup-node.sh

Installation:
* Execute ./1-build-oran.sh (ChartMuseum must be installed)

* Then choose which install
	-2-install-nonrtric-only.sh
	-2-install-oran-and-simulators-cnf.sh
	-2-install-oran-and-simulators.sh
	-2-install-oran.sh

Uninstallation:
* Execute ./uninstall-all.sh 

Note:
Installation can be customized in ./helm-override/
