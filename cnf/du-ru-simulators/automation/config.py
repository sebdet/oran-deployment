# ============LICENSE_START=======================================================
# Copyright (C) 2021 Orange
#  Modifications Copyright 2021 AT&T
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ============LICENSE_END=========================================================

class Config:
    SCENARIO = 1
    # 1 - default configuration values like set below
    # 2 - extra ssh service that comes from the profile
    # 3 - extra ssh service that comes from config + verification of the CNF status
    # change requires new onboarding

    #### REGION DETAILS ####
    COMPLEX_ID = "complex"
    CLOUD_OWNER = "k8sCloudOwner"
    CLOUD_REGION = "kud-1"
    AVAILABILITY_ZONE_NAME = "k8s-availability-zone"
    HYPERVISOR_TYPE = "k8s"
    TENANT_NAME = "kud-1"
    K8S_NAMESPACE = "oran-simulators"
    K8S_VERSION = "1.18.9"
    CUSTOMER_RESOURCE_DEFINITIONS = []
# Uncomment, if you want to run on non KUD k8s cluster
#    CUSTOMER_RESOURCE_DEFINITIONS = ["crds/crd1",
#                                     "crds/crd2"]

    CLUSTER_KUBECONFIG_PATH = "artifacts/cluster_kubeconfig"

    #### SERVICE DETAILS ####
    NATIVE = True
    SKIP_POST_INSTANTIATION = True
    GLOBAL_CUSTOMER_ID = "customer_cnf"
    VSPFILE = "vsp/oran-du-ru-simulators.zip"
    if NATIVE:
        VSPFILE = "vsp/oran-du-ru-simulators.zip"
    PROFILE_NAME = "topology-server-profile"
    PROFILE_SOURCE = PROFILE_NAME
    RELEASE_NAME = "oran-simulator-1"

    VENDOR = "vendor_cnf"
    SERVICENAME = "ORAN2_DU_RU_SIM_KUD" + "_" + str(SCENARIO)
    VSPNAME = "ORAN_VSP_" + SERVICENAME
    VFNAME = "ORAN_VF_" + SERVICENAME
    SERVICE_INSTANCE_NAME = "INSTANCE_" + SERVICENAME + "_1"
    SDNC_ARTIFACT_NAME = "vnf"

    # INSERT PARAMS FOR VNF HERE AS "name" : "value" PAIR
    VNF_PARAM_LIST = {
        "k8s-rb-profile-namespace": K8S_NAMESPACE,
        "k8s-rb-profile-k8s-version": K8S_VERSION
    }

    VF_MODULE_PREFIX = ""
    if NATIVE:
        VF_MODULE_PREFIX = "helm_"

    VF_MODULE_PARAM_LIST = {
        VF_MODULE_PREFIX + "topology_server": {
            "k8s-rb-profile-name": PROFILE_NAME,
            "k8s-rb-profile-source": PROFILE_SOURCE,
            "k8s-rb-instance-release-name": RELEASE_NAME + "-topology-server"
        },
        VF_MODULE_PREFIX + "du_simulator": {
            "k8s-rb-profile-name": PROFILE_NAME,
            "k8s-rb-profile-source": PROFILE_SOURCE,
            "k8s-rb-instance-release-name": RELEASE_NAME + "-du-simulator"
        },
        VF_MODULE_PREFIX + "ru_simulator": {
            "k8s-rb-profile-name": PROFILE_NAME,
            "k8s-rb-profile-source": PROFILE_SOURCE,
            "k8s-rb-instance-release-name": RELEASE_NAME + "-ru-simulator"
        }
    }

    ######## DEFAULT VALUES ########
    OWNING_ENTITY = "OE-Demonstration"
    PROJECT = "Project-Demonstration"
    PLATFORM = "test"
    LINE_OF_BUSINESS = "LOB-Demonstration"

    ######## SCENARIOS #############

    ########     1    #############
    if SCENARIO == 1:
        SKIP_POST_INSTANTIATION = True
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-name"] = PROFILE_NAME
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-source"] = PROFILE_SOURCE
    ########     2    #############
    elif SCENARIO == 2:
        SKIP_POST_INSTANTIATION = True
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-name"] = "vfw-cnf-cds-vpkg-profile"
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-source"] = "vfw-cnf-cds-vpkg-profile"
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["vpg-management-port"] = "31922"
    ########     3    #############
    elif SCENARIO == 3:
        SKIP_POST_INSTANTIATION = False
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-name"] = PROFILE_NAME
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-profile-source"] = PROFILE_SOURCE
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-config-template-name"] = "ssh-service-config"
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-config-template-source"] = "ssh-service-config"
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-config-name"] = "ssh-service-config"
#        VF_MODULE_PARAM_LIST[VF_MODULE_PREFIX + "vpkg"]["k8s-rb-config-value-source"] = "ssh-service-config"
    else:
        raise Exception("Not Implemented Scenario")

