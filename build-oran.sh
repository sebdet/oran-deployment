#!/bin/bash
echo '### Building ONAP part###'
(cd onap_oom/kubernetes && make all -e SKIP_LINT=TRUE)
echo  '### Building ORAN part ###'
(cd oran_oom && make all)
