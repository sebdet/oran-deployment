#!/bin/bash
helm plugin install ../onap_oom/kubernetes/helm/plugins/undeploy/
helm plugin install ../onap_oom/kubernetes/helm/plugins/deploy/
helm plugin install https://github.com/chartmuseum/helm-push.git

helm repo add local http://localhost:18080

echo '### Building ONAP part###'
(cd ../onap_oom/kubernetes && make all -e SKIP_LINT=TRUE)
echo  '### Building ORAN part ###'
(cd ../oran_oom && make all)
