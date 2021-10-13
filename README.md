# ORAN SMO Package

This project investigates how different helm charts from different Linux Foundation projects can be integrated into one common deployment, in terms of installation but also in terms of configuration.
The ONAP and ORAN project helm charts are built and then configured by using "helm override" so that it represents a valid ORAN SMO installation.
It contains also provisioning scripts that can be used to bootstrap the platform and eecute some usecases, network simulators, a1 simulators, cnf network simulators, etc ...

<strong>Note:</strong>
The CNF part is still a "work in progress" so not well documented, it's a DU/RU/topology server deployment done by ONAP SO instantiation.
It has been created out of the ONAP vfirewall usecase.

## Download:
Use git clone to get it on your server (github ssh key config is required):

```git clone --recursive git@github.com:gmngueko/oran-deployment.git```


<strong>Note:</strong> The current repository has multiple sub git submodules, therefore the <strong>--recursive</strong> flag is absolutely <strong>REQUIRED</strong>
  
## Requirements:
* K8S node setup with Helm 3 and Kubectl properly configured (tested with <strong>K8S v1.21.5</strong> and <strong>HELM v3.5.4</strong>).
  FOR K8S installation, multiple options are available:
	- MicroK8S standalone deployment, this current wiki can help to setup it (<strong>Section 1, 2 and 3</strong>): https://wiki.onap.org/display/DW/Deploy+OOM+and+SDC+%28or+ONAP%29+on+a+single+VM+with+microk8s+-+Honolulu+Setup

	- KubeSpray using ONAP multicloud KUD (https://git.onap.org/multicloud/k8s/tree/kud) installation by executing(this is required for ONAP CNF deployments): 
            
	    ```cd scripts && ./0-setup-node.sh```
    

	- Use an existing K8S installation (Cloud, etc ...).
	- ....

* ChartMuseum to store the HELM charts on the server, multiple options are available:
	- Execute the install script:

		```cd scripts && 0-setup-charts-museum.sh```
	- Install chartmuseum manually on port 18080 (https://chartmuseum.com/#Instructions, https://github.com/helm/chartmuseum)
    
## Configuration:
	In the ./helm-override/ folder the helm config that are used by the installation. 
	Different flavors are preconfigured, and should NOT be changed EXCEPT for the simulators (due to DNS limitations in the simulators)
	in ./helm-override/simulators-override.yaml, the "sdnControllerIp" and "vesEndpointIp" must be set to the server external IP.

## Installation:
* Build ONAP/ORAN charts: execute "./scripts/1-build-all-charts.sh"
* Choose which installation should be deployed:
	- ORAN "nonrtric" par only: 
		"2-install-nonrtric-only.sh"

	- ONAP CNF + ORAN "nonrtric" (This must still be documented properly): 
		"2-install-oran-cnf.sh"

	- ONAP + ORAN "nonrtric" (RECOMMENDED ONE):  
		"2-install-oran.sh"

* Install the PNF simulators:
	- If all pods in "onap" and "nonrtric" namespaces are well running:
		"kubectl get pods -n onap && kubectl get pods -n nonrtric"

	- Execute the install script:
		"2-install-simulators.sh"

	- Check the simulators status 
		"kubectl get pods -n simulators"
	
## Platform access points:
* SDNR WEB: 
	https://<K8SServerIP>:30205/odlux/index.html
* NONRTRIC Dashboard: 
	http://<K8SServerIP>:30091/
  More to come ...

## Uninstallation:
* Execute ./uninstall-all.sh 
