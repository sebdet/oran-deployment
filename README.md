# o-ran-onap-based-smo-deployment

This project investigates how different helm charts from different 
Linux Foundation projects can be integrated into one deployment.

1. Download:
* Use git clone to get it on your server (github ssh key config is required):
	"git clone --recursive git@github.com:gmngueko/oran-deployment.git"
  
  Note: The current repository has multiple sub git submodules, therefore the --recursive flag is absolutely REQUIRED
  
2. Requirements:
* K8S node setup with Helm 3 and Kubectl (tested with K8S v1.21.5). 
  FOR K8S installation, different options are available:
	- MicroK8S, this current can help for microk8s steup: 
            https://wiki.onap.org/display/DW/Deploy+OOM+and+SDC+%28or+ONAP%29+on+a+single+VM+with+microk8s+-+Honolulu+Setup

	- KubeSpray using ONAP multicloud KUD installation (This is required for ONAP CNF deployment) by executing: 
            "scripts/0-setup-node.sh"   
            Additonal info on the KUD: https://git.onap.org/multicloud/k8s/tree/kud

	- Use an existing K8S installation (Cloud, etc ...). 

* ChartMuseum to store the helm charts on the server, different options are available:
	- Install chartmuseum manually on port 18080 
                https://chartmuseum.com/#Instructions
		https://github.com/helm/chartmuseum
    
	- Execute the install script:
            "0-setup-charts-museum.sh"

3. Configuration:
	In the ./helm-override/ folder the helm config that are used by the installation. 
	Different flavors are preconfigured, and should NOT be changed EXCEPT for the simulators (due to DNS limitations in the simulators)
	in ./helm-override/simulators-override.yaml, the "sdnControllerIp" and "vesEndpointIp" must be set to the server external IP.

4. Installation:
* Build ONAP/ORAN charts: execute "./scripts/1-build-all-charts.sh"
* Choose which installation should be deployed:
	- ORAN "nonrtric" par only: 
		"./scripts/2-install-nonrtric-only.sh"

	- ONAP CNF/ORAN "nonrtric"/CNF simulators (This must still be documented properly): 
		"./scripts/2-install-oran-and-simulators-cnf.sh"

	- ONAP/ORAN "nonrtric" (RECOMMENDED ONE):  
		"./scripts/2-install-oran.sh"

* Install the PNF simulators:
	- If all pods in "onap" and "nonrtric" namespaces are well running:
		"kubectl get pods -n onap && kubectl get pods -n nonrtric"

	- Execute the install script:
		"./scripts/2-install-simulators.sh"

	- Check the simulators status 
		"kubectl get pods -n simulators"
	
5. Platform access points:
* SDNR WEB: 
	https://<K8SServerIP>:30205/odlux/index.html
* NONRTRIC Dashboard: 
	http://<K8SServerIP>:30091/
  More to come ...

6. Uninstallation:
* Execute ./uninstall-all.sh 
