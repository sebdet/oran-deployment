"""Specific settings module."""  # pylint: disable=bad-whitespace,line-too-long
import subprocess

######################
#                    #
# ONAP INPUTS DATAS  #
#                    #
######################


# Variables to set logger information
# Possible values for logging levels in onapsdk: INFO, DEBUG , WARNING, ERROR
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "class": "logging.Formatter",
            "format": "%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "pythonsdk.debug.log",
            "mode": "w"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
}

######################
#                    #
# ONAP SERVICES URLS #
#                    #
######################

AAI_URL         = "https://aai.api.sparky.simpledemo.onap.org:30233"
AAI_API_VERSION = "v23"
AAI_AUTH        = "Basic QUFJOkFBSQ=="
CDS_URL         = "http://portal.api.simpledemo.onap.org:30449"
CDS_AUTH        = ("ccsdkapps", "ccsdkapps")
MSB_URL         = "https://msb.api.simpledemo.onap.org:30283"
SDC_BE_URL      = "https://sdc.api.be.simpledemo.onap.org:30204"
SDC_FE_URL      = "https://sdc.api.fe.simpledemo.onap.org:30207"
SDC_AUTH        = "Basic YWFpOktwOGJKNFNYc3pNMFdYbGhhazNlSGxjc2UyZ0F3ODR2YW9HR21KdlV5MlU="
#SDNC_URL        = "https://sdnc.api.simpledemo.onap.org:30267"
SDNC_AUTH       = "Basic YWRtaW46S3A4Yko0U1hzek0wV1hsaGFrM2VIbGNzZTJnQXc4NHZhb0dHbUp2VXkyVQ=="
SO_URL          = "http://so.api.simpledemo.onap.org:30277"
SO_API_VERSION  = "v7"
SO_AUTH         = "Basic SW5mcmFQb3J0YWxDbGllbnQ6cGFzc3dvcmQxJA=="
VID_URL         = "https://vid.api.simpledemo.onap.org:30200"
VID_API_VERSION = "/vid"
CLAMP_AUTH      = "Basic ZGVtb0BwZW9wbGUub3NhYWYub3JnOmRlbW8xMjM0NTYh"
VES_URL         = "http://ves.api.simpledemo.onap.org:30417"
DMAAP_URL       = "http://192.168.1.39:3904"
NBI_URL         = "https://nbi.api.simpledemo.onap.org:30274"
NBI_API_VERSION = "/nbi/api/v4"

POLICY_BASICAUTH = { 'username': 'policyadmin', 'password': 'zb!XztG34' }
SDNC_BASICAUTH = { 'username': 'admin', 'password': 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U' }
CLAMP_BASICAUTH = { 'username': 'demo@people.osaaf.org', 'password': 'demo123456!' }

DMAAP_URL = "http://"+subprocess.run("kubectl get services message-router -n onap |grep message-router | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":3904"

A1SIM_OSC_URL = "http://"+subprocess.run("kubectl get services a1-sim-osc-0 -n nonrtric |grep a1-sim-osc-0 | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":8085"
A1SIM_STD1_URL = "http://"+subprocess.run("kubectl get services a1-sim-std1-0 -n nonrtric |grep a1-sim-std1-0 | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":3904"
A1SIM_STD2_URL = "http://"+subprocess.run("kubectl get services a1-sim-std2-0 -n nonrtric |grep a1-sim-std2-0 | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":3904"

POLICY_PAP_URL = "https://"+subprocess.run("kubectl get services policy-pap -n onap |grep policy-pap | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":6969"
POLICY_API_URL = "https://"+subprocess.run("kubectl get services policy-api -n onap |grep policy-api | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":6969"
SDNC_URL = "http://"+subprocess.run("kubectl get services sdnc-oam -n onap |grep sdnc-oam | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":8282"
CLAMP_URL = "https://"+subprocess.run("kubectl get services policy-clamp-be -n onap |grep policy-clamp-be | awk '{print $3}'", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()+":8443"

### Network simulators topology
NETWORK_SIMULATORS_RU_LIST = ["o-ru-11211","o-ru-11221","o-ru-11222","o-ru-11223"]
NETWORK_SIMULATORS_DU_LIST = ["o-du-1121","o-du-1122"]
NETWORK_SIMULATORS_TOPOLOGY_SERVER = ["topology-server"]
NETWORK_SIMULATORS_DU_RU_LIST = NETWORK_SIMULATORS_DU_LIST + NETWORK_SIMULATORS_RU_LIST
NETWORK_SIMULATORS_LIST = NETWORK_SIMULATORS_DU_RU_LIST + NETWORK_SIMULATORS_TOPOLOGY_SERVER
DMAAP_GROUP = "o1test"
DMAAP_USER = "o1test"
DMAAP_CL_GROUP = "cltest"
DMAAP_CL_USER = "cltest"
DMAAP_TOPIC_PNFREG = "unauthenticated.VES_PNFREG_OUTPUT"
DMAAP_TOPIC_PNFREG_JSON = '{"topicName": "' + DMAAP_TOPIC_PNFREG + '", "replicationCount": 1}'
DMAAP_TOPIC_FAULT = "unauthenticated.SEC_FAULT_OUTPUT"
DMAAP_TOPIC_FAULT_JSON = '{"topicName": "' + DMAAP_TOPIC_FAULT + '", "replicationCount": 1}'

### Number of pods left in completed state for ONAP namespace
ONAP_PODS_WHEN_READY = 9
SMO_CHECK_RETRY = 30
SMO_CHECK_TIMEOUT = 900
SDNC_CHECK_RETRY = 30
SDNC_CHECK_TIMEOUT = 900
POLICY_CHECK_RETRY = 30
POLICY_CHECK_TIMEOUT = 900
CLAMP_CHECK_RETRY = 30
CLAMP_CHECK_TIMEOUT = 900
NETWORK_SIMULATOR_CHECK_RETRY = 30
NETWORK_SIMULATOR_CHECK_TIMEOUT = 900
