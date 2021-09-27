#!/bin/bash
./sub-scripts/install-onap.sh ../helm-override/onap-override.yaml
./sub-scripts/install-nonrtric.sh ../helm-override/oran-override.yaml
