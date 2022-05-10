# ORAN SMO Package

This project uses different helm charts from different Linux Foundation projects and integrate them into a unique SMO deployment.
<p>The ONAP and ORAN project helm charts are built and then configured by using "helm override" so that it represents a valid ORAN SMO installation.</p>
<p>It contains also provisioning scripts that can be used to bootstrap the platform and execute test usecases, network simulators, a1 simulators, cnf network simulators, etc ...</p>

<strong>Note:</strong>
The CNF part is still a "work in progress" so not well documented, it's a DU/RU/topology server deployment done by ONAP SO instantiation.
It has been created out of the ONAP vfirewall usecase.

## Quick Installation on blank node
* Setup a VM with 40GB Memory, 6VCPU, 60GB of diskspace. 
* Install an ubuntu live server 20.04 LTS (https://releases.ubuntu.com/20.04/ubuntu-20.04.3-live-server-amd64.iso)
* Install snap and restart the shell session: sudo apt-get install snapd -y
* Execute the following commands being logged as root:


	```git clone --recursive https://github.com/sebdet/oran-deployment.git```

	```./oran-deployment/scripts/layer-0/0-setup-microk8s.sh```

	```./oran-deployment/scripts/layer-0/0-setup-charts-museum.sh```
	
	```./oran-deployment/scripts/layer-0/0-setup-helm3.sh```
	
	```./oran-deployment/scripts/layer-1/1-build-all-charts.sh```

	```./oran-deployment/scripts/layer-2/2-install-oran.sh```

	Verify pods:

	```kubectl get pods -n onap && kubectl get pods -n nonrtric```
	
	When all pods in "onap" and "nonrtric" namespaces are well up & running:
	
	```./oran-deployment/scripts/layer-2/2-install-simulators.sh```

## Quick Installation on existing kubernetes
* Ensure you have at least 20GB Memory, 6VCPU, 60GB of diskspace. 
* Execute the following commands being logged as root:

	```git clone --recursive git@github.com:gmngueko/oran-deployment.git```

	```./oran-deployment/scripts/layer-0/0-setup-charts-museum.sh```
	
	```./oran-deployment/scripts/layer-0/0-setup-helm3.sh```
	
	```./oran-deployment/scripts/layer-1/1-build-all-charts.sh```

	```./oran-deployment/scripts/layer-2/2-install-oran.sh```

	Verify pods:

	```kubectl get pods -n onap && kubectl get pods -n nonrtric```
	
	When all pods in "onap" and "nonrtric" namespaces are well up & running:
	
	```./oran-deployment/scripts/layer-2/2-install-simulators.sh```


## Structure
The user entry point is located in the <strong>scripts</strong> folder

```
.
├── cnf				<-- CNF packages that can be deployed by ONAP (Work In Progress, so not yet well documented)
│   └── du-ru-simulators		<--- The CNF package containing DU/RU/Topology server simulators
├── helm-override		<-- The Configuration of the different HELM charts used in SMO package
│   ├── network-simulators-override.yaml		<--- Standard config for the network simulators
│   ├── network-simulators-topology-override.yaml	<--- Network simulator topology example that can be changed
│   ├── onap-override-cnf.yaml		<--- A medium ONAP config ready for CNF deployment
│   ├── onap-override.yaml		<--- A minimal ONAP config for SMO package
│   └── oran-override.yaml		<--- A minimal ORAN config for SMO package
├── LICENSE
├── multicloud-k8s		<-- Git SUBMODULE required for KUD installation
├── onap_oom			<-- Git SUBMODULE required for ONAP installation
├── oran_oom			<-- ORAN Charts
│   ├── a1controller
│   ├── a1simulator
│   ├── aux-common
│   ├── controlpanel
│   ├── dist
│   ├── dmaapadapterservice
│   ├── du-simulator
│   ├── enrichmentservice
│   ├── Makefile		<-- ORAN Makefile to build all ORAN Charts
│   ├── nonrtric
│   ├── nonrtric-common
│   ├── nonrtricgateway
│   ├── oru-app
│   ├── policymanagementservice
│   ├── rappcatalogueservice
│   ├── ric-common
│   ├── ru-du-simulators
│   ├── ru-simulator
│   ├── topology
│   └── topology-server
├── README.md
├── scripts			<-- All installation scripts (USER ENTRY POINT)
│   ├── layer-0				<--- Scripts to setup Node
│   │   ├── 0-setup-charts-museum.sh		<--- Setup ChartMuseum
│   │   └── 0-setup-kud-node.sh			<--- Setup K8S node with ONAP Multicloud KUD installation
│   │   └── 0-setup-microk8s.sh		<--- Setup K8S node with MicroK8S installation
│   │   └── 0-setup-helm3.sh			<--- Setup HELM3
│   ├── layer-1				<--- Scripts to prepare for the SMO installation
│   │   └── 1-build-all-charts.sh		<--- Build all HELM charts and upload them to ChartMuseum
│   ├── layer-2				<--- Scripts to install SMO package
│   │   ├── 2-install-nonrtric-only.sh		<--- Install SMO NONRTRIC k8s namespace only
│   │   ├── 2-install-oran-cnf.sh		<--- Install SMO full with ONAP CNF features
│   │   ├── 2-install-oran.sh			<--- Install SMO minimal 
│   │   └── 2-install-simulators.sh		<--- Install Network simulator (RU/DU/Topology Server)
│   │   └── 2-upgrade-simulators.sh		<--- Upgrade the simulators install at runtime when changes are done on override files
│   ├── sub-scripts			<--- Sub-Scripts used by the main layer-0, layer-1, layer-2
│   │   ├── clean-up.sh
│   │   ├── install-nonrtric.sh
│   │   ├── install-onap.sh
│   │   ├── install-simulators.sh
│   │   ├── uninstall-nonrtric.sh
│   │   ├── uninstall-onap.sh
│   │   └── uninstall-simulators.sh
│   └── uninstall-all.sh		<--- Uninstall ALL SMO K8S namespaces and cleanup K8S
└── test			<-- Scripts to test the SMO installation (Work In Progress, so not yet well documented)
    ├── a1-validation			<--- Test nonrtric A1 interface (https://wiki.o-ran-sc.org/display/RICNR/Testing+End+to+End+call+in+release+D)
    │   ├── data
    │   ├── subscripts
    │   └── validate-a1.sh
    ├── apex-policy-test		<--- Test apex policy (https://wiki.o-ran-sc.org/pages/viewpage.action?pageId=35881325, it requires simulators to be up)
    │   ├── apex-policy-test.sh
    │   └── data
    ├── enable-sim-fault-report		<--- Enable the fault reporting of the network simulators by SDNC
    │   ├── data
    │   └── enable-network-sim-fault-reporting.sh
    └── pythonsdk			<--- Test based on ONAP Python SDK to validate O1 and A1
        ├── oran-tests.xml
        ├── Pipfile.lock
        ├── README.md
        ├── src
        ├── test.json
        ├── tox.ini
        └── unit-tests

```
## Download:
Use git clone to get it on your server (github ssh key config is required):

```git clone --recursive git@github.com:gmngueko/oran-deployment.git```


<strong>Note:</strong> The current repository has multiple sub git submodules, therefore the <strong>--recursive</strong> flag is absolutely <strong>REQUIRED</strong>
  
## Requirements:
* K8S node setup with Helm 3 and Kubectl properly configured (tested with <strong>K8S v1.21.5</strong> and <strong>HELM v3.5.4</strong>).
  FOR K8S installation, multiple options are available:
	- MicroK8S standalone deployment:

		```./oran-deployment/scripts/layer-0/0-setup-microk8s.sh```

		OR this wiki can help to setup it (<strong>Section 1, 2 and 3</strong>): https://wiki.onap.org/display/DW/Deploy+OOM+and+SDC+%28or+ONAP%29+on+a+single+VM+with+microk8s+-+Honolulu+Setup

	- KubeSpray using ONAP multicloud KUD (https://git.onap.org/multicloud/k8s/tree/kud) installation by executing(this is required for ONAP CNF deployments): 
            
	    ```./oran-deployment/scripts/layer-0/0-setup-kud-node.sh```
    

	- Use an existing K8S installation (Cloud, etc ...).
	- ....

* ChartMuseum to store the HELM charts on the server, multiple options are available:
	- Execute the install script:

		```./oran-deployment/scripts/layer-0/0-setup-charts-museum.sh```
		
		```./oran-deployment/scripts/layer-0/0-setup-helm3.sh```

	- Install chartmuseum manually on port 18080 (https://chartmuseum.com/#Instructions, https://github.com/helm/chartmuseum)
    
## Configuration:
In the ./helm-override/ folder the helm config that are used by the SMO installation. 
<p>Different flavors are preconfigured, and should NOT be changed unless you intentionally want to updates some configurations.

## Installation:
* Build ONAP/ORAN charts 

	```./oran-deployment/scripts/layer-1/1-build-all-charts.sh```

* Choose the installation:
	- ONAP + ORAN "nonrtric" <strong>(RECOMMENDED ONE)</strong>:  
	
		```./oran-deployment/scripts/layer-2/2-install-oran.sh```
	- ORAN "nonrtric" par only: 
	
		```./oran-deployment/scripts/layer-2/2-install-nonrtric-only.sh```

	- ONAP CNF + ORAN "nonrtric" (This must still be documented properly): 

		```./oran-deployment/scripts/layer-2/2-install-oran-cnf.sh```



* Install the network simulators (DU/RU/Topo):
	- When all pods in "onap" and "nonrtric" namespaces are well up & running:
		
		```kubectl get pods -n onap && kubectl get pods -n nonrtric```

	- Execute the install script:
		
		```./oran-deployment/scripts/layer-2/2-install-simulators.sh```

	- Check the simulators status:

		```kubectl get pods -n network```

	Note: The simulators topology can be customized in the file ./oran-deployment/helm-override/network-simulators-topology-override.yaml

## Platform access points:
* SDNR WEB: 
	https://<K8SServerIP>:30205/odlux/index.html
* NONRTRIC Dashboard: 
	http://<K8SServerIP>:30091/
  More to come ...

## Uninstallation:
* Execute 
	
	```./oran-deployment/scripts/uninstall-all.sh```
