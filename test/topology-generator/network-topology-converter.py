#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2021-2022 AT&T Intellectual Property. All rights
#                             reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END============================================
# ===================================================================
#
###

import json
import sys
import yaml

def read_json_topology_file (filename):
	return json.loads(open(filename, "r").read())

def save_helm_override_file (helm_file, filename):
	with open(filename, 'w') as file:
		return yaml.dump(helm_file, file)

def get_name_of_node (node):
	for name in node["name"]:
		if name["value-name"] == "topology-node-name":
			return name["value"]

def search_all_topology_nodes (topology_json):
	ru_nodes = {}
	du_nodes = {}
	ue_nodes = {}
	cu_nodes = {}
	near_rt_ric_nodes = {}
	smo_nodes = {}

	for node in topology_json["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"]:

		if node["o-ran-topology:function"] == "o-ran-common-identity-refs:o-ru-function":
			ru_nodes[get_name_of_node(node)]=node

		elif node["o-ran-topology:function"] == "o-ran-common-identity-refs:o-du-function":
			du_nodes[get_name_of_node(node)]=node
		elif node["o-ran-topology:function"] == "o-ran-common-identity-refs:user-equipment-function":
			ue_nodes[get_name_of_node(node)]=node
		elif node["o-ran-topology:function"] == "o-ran-common-identity-refs:o-cu-up-function":
			cu_nodes[get_name_of_node(node)]=node
		elif node["o-ran-topology:function"] == "o-ran-common-identity-refs:near-rt-ric-function":
			near_rt_ric_nodes[get_name_of_node(node)]=node
		elif node["o-ran-topology:function"] == "o-ran-common-identity-refs:smo-function":
			smo_nodes[get_name_of_node(node)]=node
	return {"ru_nodes":ru_nodes, "du_nodes": du_nodes, "ue_nodes": ue_nodes, "cu_nodes": cu_nodes, "near_rt_ric_nodes":near_rt_ric_nodes, "smo_nodes":smo_nodes}

def generate_ru_node (ru_nodes):
	rus=[]
	for ru_key in ru_nodes:
		rus.append({"name":ru_key, "simulatedFaults":[]})
	return {"ru_simulator":{"rus":rus}}

def generate_ru_faults ():
	return {}

all_nodes=search_all_topology_nodes(read_json_topology_file (sys.argv[1]))
helm_override={}
helm_override = {**helm_override, **generate_ru_node(all_nodes["ru_nodes"])}


print ("#RU:"+str(len(all_nodes["ru_nodes"])))
print ("#DU:"+str(len(all_nodes["du_nodes"])))
print ("#UE:"+str(len(all_nodes["ue_nodes"])))
print ("#CU:"+str(len(all_nodes["cu_nodes"])))
print ("#NEAR_RTRIC:"+str(len(all_nodes["near_rt_ric_nodes"])))
print ("#SMO:"+str(len(all_nodes["smo_nodes"])))
number_of_nodes=len(all_nodes["ru_nodes"])+len(all_nodes["du_nodes"])+len(all_nodes["ue_nodes"])+len(all_nodes["cu_nodes"])+len(all_nodes["near_rt_ric_nodes"])+len(all_nodes["smo_nodes"])
print ("#Nodes(total):"+str(number_of_nodes))

print(save_helm_override_file(helm_override, sys.argv[2]))
