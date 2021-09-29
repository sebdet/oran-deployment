#!/bin/bash

curl https://raw.githubusercontent.com/helm/chartmuseum/main/scripts/get-chartmuseum | bash
mkdir ./chartmuseum
chartmuseum --port=8080 --storage="local" --storage-local-rootdir="./chartstorage" &
