#!/usr/bin/env python3.8
################################################################################
# Copyright 2021 highstreet technologies GmbH
####################################################################
# Modifications Copyright (C) 2021 AT&T
####################################################################
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# importing the sys, json, requests library
import os
import sys
import json
import requests
import subprocess

dockerFilter = subprocess.check_output("kubectl get services -n network -o name | awk -F \"/\" '{print $2}'", shell=True)
containers = dockerFilter.splitlines()
dockerSdnc = subprocess.check_output("kubectl get services sdnc-web-service -n onap | grep sdnc-web-service |  awk '{print $3}'", shell=True)

mapping = dict({"ntsim-ng-o-ru": "o-ru", "ntsim-ng-o-du": "o-du"}) 
# base = 'https://sdnc-web:8453'
base = 'https://'+ dockerSdnc.decode("utf-8").strip() +':8443'
username = 'admin'
password = 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U'

# REST to set event settings
def configEventSettings(nfName, nfType):
  file = os.path.dirname(os.path.abspath(__file__)) + '/data/' + 'event-settings-'+nfType+'.json'
  print ("File name:" + file)
  with open(file) as json_file:
    body = json.load(json_file)
    url = base + '/rests/data/network-topology:network-topology/topology=topology-netconf/node=' + nfName + '/yang-ext:mount/nts-network-function:simulation/network-function'
    print ("url:"+url)
    headers = {
        'content-type': 'application/yang-data+json',
        'accept': 'application/yang-data+json'
    }
    try:
      response = requests.put(url, verify=False, auth=(username, password), json=body, headers=headers)
      print("Response:" + str(response))
    except requests.exceptions.Timeout:
      sys.exit('HTTP request failed, please check you internet connection.')
    except requests.exceptions.TooManyRedirects:
      sys.exit('HTTP request failed, please check your proxy settings.')
    except requests.exceptions.RequestException as e:
      # catastrophic error. bail.
      raise SystemExit(e)

    return response.status_code >= 200 and response.status_code < 300

# main
print ("Container Lines:"+str(containers))
for container in containers:
  name = container.decode("utf-8")
  if "o-" in name:
    if "o-ru" in name:
      print("Set", name, configEventSettings(name, "ru"))
    if "o-du" in name:
      print("Set", name, configEventSettings(name, "du"))
