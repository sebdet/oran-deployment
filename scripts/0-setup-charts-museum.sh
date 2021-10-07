#!/bin/bash

curl https://raw.githubusercontent.com/helm/chartmuseum/main/scripts/get-chartmuseum | bash
chartmuseum --port=18080 --storage="local" --storage-local-rootdir="./chartstorage" &
