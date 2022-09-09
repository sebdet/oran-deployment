# Automate Network Slicing tests using SMO Package

SMO package could be used in different ways. Here is the summary about how to use SMO package to automate the Network Slicing tests.

There is also a wiki page regarding using SMO package to automate the Network Slicing tests. Please check the link below:
https://wiki.onap.org/display/DW/Automate+Netwok+Slicing+Use+case+option2+using+SMO+package

## Download:
Use git clone to get it on your server (github ssh key config is required):

```git clone --recursive git@github.com:gmngueko/oran-deployment.git```


<strong>Note:</strong> The current repository has multiple sub git submodules, therefore the <strong>--recursive</strong> flag is absolutely <strong>REQUIRED</strong>
  
## Requirements:
* To deploy and test the network slicing use case, you need some basic softwares installed in your lab. You can run the following script for the installation.

  ```git clone --recursive git@github.com:gmngueko/oran-deployment.git```

  ```./oran-deployment/scripts/layer-0/0-setup-charts-museum.sh```

  ```./oran-deployment/scripts/layer-0/0-setup-helm3.sh```

  ```./oran-deployment/scripts/layer-0/0-setup-microk8s.sh```

  ```./oran-deployment/scripts/layer-0/0-setup-tests-env.sh```
    

## Deploy ONAP:
* Before the deployment, need to build the helm charts 

	```./oran-deployment/scripts/layer-1/1-build-all-charts.sh```

* Deploy ONAP for the Network Slicing Option2 use case:
  
	```./oran-deployment/scripts/layer-2/2-install-onap-only.sh network-slicing```

* After the deployment, please verify the pods:
  
	```kubectl get pods -n onap```


## Run test script:
* When all the ONAP components are up and running, go to network_slicing folder and run the test script with tox command:
  
	```cd ./oran-deployment/test/pythonsdk/src/orantests/network_slicing```
	```tox -e ns-tests```

## Uninstallation:
* Execute 
	
	```./oran-deployment/scripts/uninstall-all.sh```
