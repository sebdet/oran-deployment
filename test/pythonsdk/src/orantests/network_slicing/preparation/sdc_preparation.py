#!/usr/bin/env python3
###
# ============LICENSE_START===================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
#  Copyright (C) 2021 Samsung Electronics
#  Copyright (C) 2022 AT&T Intellectual Property. All rights
#                             reserved.
# ============================================================================
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
# SPDX-License-Identifier: Apache-2.0
# ============LICENSE_END=====================================================
#
###
"""Create SDC Templates for Network Slicing option2 test."""
import logging
import logging.config
from time import sleep
import os
from onapsdk.sdc.vfc import Vfc
from onapsdk.sdc.vf import Vf
import onapsdk.constants as const
from onapsdk.configuration import settings
from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc.properties import Property, ParameterError
from waiting import wait
from oransdk.aai.service_design_and_creation import AaiModel
from oransdk.sdc.sdc import SdcTemplate
from oransdk.sdc.service import OranService

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start SDC Preparation")
service_dict = {}
service_list = []

class SdcPreparation():
    """Can be used to prepare SDC for Network Slicing usecase option2."""

    def __init__(self, suffix: str = None):
        """
        Initialize SDC preparation object.

        Args:
            suffix (str, optional): the suffix of the SDC template names

        """
        if suffix is None:
            self.suffix = ""
        else:
            self.suffix = suffix

    def prepare_sdc(self) -> dict:
        """Create SDC templates."""
        # Populate AAI needed value

        sdc = SdcTemplate()
        vendor = sdc.create_vendor('ONAP')
        sdc.create_vsp('test1', vendor)

        # 0.create custom categories
        logger.info("####################### create custom categories")
        sdc.create_service_category(['CST', 'ServiceProfile', 'AN SliceProfile', 'CN SliceProfile', 'TN SliceProfile',
                                     'NST', 'TN BH NSST', 'TN Network Requirement', 'AN NF NSST', 'CN NSST', 'Allotted Resource'])


        vf_tn_bh_ar = self.create_tn_resources(sdc, vendor)
        vf_embban_nf_ar = self.create_an_resources(sdc, vendor)
        vf_embbcn_external_ar = self.create_cn_resources(sdc, vendor)
        self.create_nst(sdc, vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar)

        vf_slice_ar = self.create_slice_ar(sdc, vendor)

        srv_slice_profile_an_o2 = self.create_an_slice_profiles(sdc, vf_slice_ar)
        srv_slice_profile_tn = self.create_tn_slice_profiles(sdc, vf_slice_ar)
        srv_slice_profile_cn = self.create_cn_slice_profiles(sdc, vf_slice_ar)
        srv_profile_o2 = self.create_service_profile(sdc, vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2)
        cst = self.create_cst(sdc, srv_profile_o2)
        wait(lambda: self.verify_distribution(), sleep_seconds=60, timeout_seconds=3600, waiting_for="All services distributed successfully")
        return [cst.identifier, cst.unique_uuid, srv_profile_o2.identifier]

    def create_tn_resources(self, sdc, vendor) -> dict:
        """Create TN related resources."""
        # 1.Create TN_Network_Requirement Service
        logger.info("####################### create TN_Network_Requirement Service")
        props = [Property('ConnectionLink', 'string'),
                 Property('jitter', 'string', value='10'),
                 Property('latency', 'integer', value=10),
                 Property('maxBandwith', 'integer', value=1000)]

        srv_tn_network = sdc.create_service(self.updated_name('TN_Network_Requirement'), 'TN Network Requirement', properties=props,
                                            inputs=[Property('ConnectionLink', 'string')])
        service_dict[srv_tn_network.identifier] = False
        service_list.append(srv_tn_network)

        # 2.Create TN_Network_Req_AR
        logger.info("####################### create TN_Network_Req_AR")
        vf = sdc.create_vf(self.updated_name('TN_Network_Req_AR'), 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_tn_network.unique_uuid
                c.get_property('providing_service_uuid').value = srv_tn_network.identifier
                c.get_property('providing_service_name').value = srv_tn_network.name
                break
        sdc.onboard_vf(vf)

        # 3.Create Tn_ONAP_internal_BH Service
        logger.info("####################### create Tn_ONAP_internal_BH Service")
        props = [Property('pLMNIdList', 'string', value='39-00'),
                 Property('jitter', 'string', value='10'),
                 Property('latency', 'integer', value=10),
                 Property('maxBandwith', 'integer', value=1000)]

        srv_tn_bh = sdc.create_service(self.updated_name('Tn_ONAP_internal_BH'), 'TN BH NSST', vnfs=[vf],
                                       role='ONAP_internal', properties=props)
        service_dict[srv_tn_bh.identifier] = False
        service_list.append(srv_tn_bh)

        # 6.Create Tn_BH_AR
        logger.info("####################### Create Tn_BH_AR")
        vf_tn_bh_ar = sdc.create_vf(self.updated_name('Tn_BH_AR'), 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_tn_bh_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_tn_bh.unique_uuid
                c.get_property('providing_service_uuid').value = srv_tn_bh.identifier
                c.get_property('providing_service_name').value = srv_tn_bh.name
                break
        sdc.onboard_vf(vf_tn_bh_ar)
        return vf_tn_bh_ar

    def create_an_resources(self, sdc, vendor) -> dict:
        """Create AN related resources."""
        # 4.Create EmbbAn_NF Service Template
        logger.info("####################### create EmbbAn_NF Service Template")
        props = [Property('anNSSCap', 'org.openecomp.datatypes.NSSCapabilities')]
        srv_embban_nf = sdc.create_service(self.updated_name('EmbbAn_NF'), 'AN NF NSST', role='huawei', service_type='embb', properties=props)
        service_dict[srv_embban_nf.identifier] = False
        service_list.append(srv_embban_nf)

        # 7.Create EmbbAn_NF_AR
        logger.info("####################### create EmbbAn_NF_AR")
        vf_embban_nf_ar = sdc.create_vf(self.updated_name('EmbbAn_NF_AR'), 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_embban_nf_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_embban_nf.unique_uuid
                c.get_property('providing_service_uuid').value = srv_embban_nf.identifier
                c.get_property('providing_service_name').value = srv_embban_nf.name
                break
        sdc.onboard_vf(vf_embban_nf_ar)
        return vf_embban_nf_ar

    def create_cn_resources(self, sdc, vendor) -> dict:
        """Create CN related resources."""
        # 5.Create EmbbCn_External Service Template
        logger.info("####################### create EmbbCn_External Service Template")
        srv_embbcn = OranService(name=self.updated_name('EmbbCn_External'),
                                 category='CN NSST',
                                 role='huawei',
                                 service_type='embb',
                                 properties=[Property('cnCap', 'org.openecomp.datatypes.NSSCapabilities',\
                                                      value="{\\\"latency\\\":20,\\\"maxNumberofUEs\\\":10000,\
                                                              \\\"resourceSharingLevel\\\":\\\"Shared\\\",\\\"sST\\\":\\\"eMBB\\\",\
                                                              \\\"activityFactor\\\":30,\\\"areaTrafficCapDL\\\":800,\
                                                              \\\"areaTrafficCapUL\\\":800,\\\"expDataRateDL\\\":1000,\
                                                              \\\"survivalTime\\\":10,\\\"uEMobilityLevel\\\":\\\"stationary\\\",\
                                                              \\\"expDataRateUL\\\":1000,\\\"pLMNIdList\\\":\\\"39-00\\\"}")])

        srv_embbcn.create()

        if srv_embbcn.status == const.DRAFT:
            srv_embbcn.add_deployment_artifact(artifact_type="WORKFLOW", artifact_name="eMBB.zip", artifact="../resources/eMBB.zip",
                                               artifact_label="abc")

        if srv_embbcn.status != const.DISTRIBUTED:
            done = False
            retry = 0
            to = 1
            while not done:
                try:
                    srv_embbcn.onboard()
                except ResourceNotFound as e:
                    retry += 1
                    if retry > 5:
                        raise e
                    to = 2 * to + 1
                    sleep(to)
                else:
                    done = True
        service_dict[srv_embbcn.identifier] = False
        service_list.append(srv_embbcn)

        # 8.EmbbCn_External_AR
        logger.info("####################### create EmbbCn_External_AR")
        vf_embbcn_external_ar = sdc.create_vf(self.updated_name('EmbbCn_External_AR'), 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_embbcn_external_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_embbcn.unique_uuid
                c.get_property('providing_service_uuid').value = srv_embbcn.identifier
                c.get_property('providing_service_name').value = srv_embbcn.name
                break
        sdc.onboard_vf(vf_embbcn_external_ar)
        return vf_embbcn_external_ar

    def create_nst(self, sdc, vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar) -> None:
        """Create NST."""
        # 9.Create EmbbNst_O2 Service Template
        logger.info("####################### create service EmbbNst_O2")
        props = [Property('latency', 'integer', value=20),
                 Property('maxNumberofUEs', 'integer', value=1000),
                 Property('maxNumberofConns', 'integer', value=100000),
                 Property('resourceSharingLevel', 'string', value='Shared'),
                 Property('sST', 'string', value='eMBB'),
                 Property('activityFactor', 'integer', value=60),
                 Property('availability', 'float', value=0.6),
                 Property('dLThptPerSlice', 'integer', value=1000),
                 Property('uLThptPerSlice', 'integer', value=1000),
                 Property('jitter', 'integer', value=10),
                 Property('survivalTime', 'integer', value=10),
                 Property('uEMobilityLevel', 'string', value='stationary'),
                 Property('pLMNIdList', 'string', value='39-00'),
                 Property('reliability', 'string', value='99%')]
        nst = sdc.create_service(self.updated_name('EmbbNst_O2'),
                                 'NST',
                                 role='option2',
                                 vnfs=[vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar],
                                 properties=props)
        service_dict[nst.identifier] = False
        service_list.append(nst)

    def create_slice_ar(self, sdc, vendor) -> dict:
        """Create Slice AR."""
        # 10. create Slice_AR
        logger.info("####################### create Slice_AR")

        vfc = Vfc('AllottedResource')
        vf_slice_ar = Vf(name=self.updated_name('Slice_AR'), category='Allotted Resource', subcategory='Allotted Resource', vendor=vendor)
        vf_slice_ar.create()
        if vf_slice_ar.status == const.DRAFT:
            vf_slice_ar.add_resource(vfc)

        for c in vf_slice_ar.components:
            if c.name == 'AllottedResource 0':
                cp = sdc.get_component_property(c, 'providing_service_invariant_uuid')
                if cp:
                    logger.info('declare input for property [%s]', cp)
                    vf_slice_ar.declare_input(cp)
                else:
                    raise ParameterError('no property providing_service_invariant_uuid found')

                cp = sdc.get_component_property(c, 'providing_service_uuid')
                if cp:
                    logger.info('declare input for property [%s]', cp)
                    vf_slice_ar.declare_input(cp)
                else:
                    raise ParameterError('no property providing_service_uuid found')

                break

        sdc.onboard_vf(vf_slice_ar)
        # AAI bug workaround: create Slice_ar in AAI DB before SO distribution, otherwise service will not be deployed to AAI succesfully
        aai = AaiModel(invariant_id=vf_slice_ar.unique_uuid, model_type="resource", resource_version=vf_slice_ar.version)
        aai.create(vf_slice_ar.name, vf_slice_ar.identifier, aai.invariant_id)
        return vf_slice_ar

    def create_an_slice_profiles(self, sdc, vf_slice_ar) -> dict:
        """Create AN Slice profile."""
        # 11.Create SliceProfile_AN_O2 Service Template
        logger.info("####################### create SliceProfile_AN_O2 Service Template")
        an_slice_profile = [Property('ipAddress', 'string'),
                            Property('logicInterfaceId', 'string'),
                            Property('nextHopInfo', 'string')]
        complex_property = Property('anSP', 'org.openecomp.datatypes.SliceProfile')
        srv_slice_profile_an_o2 = sdc.create_service_1(self.updated_name('SliceProfile_AN_O2'),
                                                       'AN SliceProfile',
                                                       properties=an_slice_profile,
                                                       inputs=an_slice_profile,
                                                       complex_input=complex_property,
                                                       vnfs=[vf_slice_ar])
        service_dict[srv_slice_profile_an_o2.identifier] = False
        service_list.append(srv_slice_profile_an_o2)
        return srv_slice_profile_an_o2

    def create_tn_slice_profiles(self, sdc, vf_slice_ar) -> dict:
        """Create TN Slice profile."""
        # 12.Create SliceProfile_TN Service Template
        logger.info('####################### create service SliceProfile_TN')
        tn_slice_profile = [Property('jitter', 'string'),
                            Property('latency', 'integer'),
                            Property('pLMNIdList', 'string'),
                            Property('sNSSAI', 'string'),
                            Property('sST', 'integer'),
                            Property('maxBandwidth', 'integer')]

        srv_slice_profile_tn = sdc.create_service_1(self.updated_name('SliceProfile_TN'),
                                                    'TN SliceProfile',
                                                    vnfs=[vf_slice_ar],
                                                    inputs=tn_slice_profile,
                                                    properties=tn_slice_profile)
        service_dict[srv_slice_profile_tn.identifier] = False
        service_list.append(srv_slice_profile_tn)
        return srv_slice_profile_tn

    def create_cn_slice_profiles(self, sdc, vf_slice_ar) -> dict:
        """Create CN Slice profile."""
        # 13.Create SliceProfile_CN Service Template
        logger.info('####################### create slice SliceProfile_CN')
        cn_slice_profile = [Property('ipAddress', 'string'),
                            Property('logicInterfaceId', 'string'),
                            Property('nextHopInfo', 'string')]
        srv_slice_profile_cn = sdc.create_service_1(self.updated_name('SliceProfile_CN'),
                                                    'CN SliceProfile',
                                                    vnfs=[vf_slice_ar],
                                                    inputs=cn_slice_profile,
                                                    properties=cn_slice_profile)
        service_dict[srv_slice_profile_cn.identifier] = False
        service_list.append(srv_slice_profile_cn)
        return srv_slice_profile_cn

    def create_service_profile(self, sdc, vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2) -> dict:
        """Create Slice profile."""
        # 14.Create ServiceProfile_O2 Service Template
        logger.info('####################### create service ServiceProfile O2')
        service_props = Property('spProp', 'org.openecomp.datatypes.ServiceProfile')
        srv_profile_o2 = sdc.create_service_1(self.updated_name('ServiceProfile_O2'),
                                              'ServiceProfile',
                                              properties=[service_props],
                                              complex_input=service_props,
                                              vnfs=[vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2],
                                              role='option2')
        service_dict[srv_profile_o2.identifier] = False
        service_list.append(srv_profile_o2)
        return srv_profile_o2

    def create_cst(self, sdc, srv_profile_o2) -> dict:
        """Create CST."""
        # 15.Create CST_O2 Service Template
        logger.info('####################### create service CST O2')
        cs_prop = Property('csProp', 'org.openecomp.datatypes.CSProperties')
        cst = sdc.create_service_1(self.updated_name('CST_O2'),
                                   'CST',
                                   role='option2',
                                   service_type='embb',
                                   vnfs=[srv_profile_o2],
                                   properties=[cs_prop],
                                   complex_input=cs_prop)
        service_dict[cst.identifier] = False
        service_list.append(cst)
        return cst

    def updated_name(self, name) -> str:
        """Adding suffix for the name."""
        return name + self.suffix

    @classmethod
    def verify_distribution(cls) -> bool:
        """Verify the distribution of all the services."""
        for service in service_list:
            logger.info('####################### verify service:%s', service.name)
            if service_dict[service.identifier]:
                continue
            so_ready = False
            aai_ready = False
            result = service.get_distribution_status()
            for element in result['distributionStatusList']:
                if (element['omfComponentID'] == "SO-COpenSource-Env11" and (element['status'] == "DEPLOY_OK" or element['status'] == const.DOWNLOAD_OK)):
                    so_ready = True
                if (element['omfComponentID'] == "aai-ml" and element['status'] == "DEPLOY_OK"):
                    aai_ready = True
            if so_ready and aai_ready:
                service_dict[service.identifier] = True
                logger.info('####################### service %s distributed successfully to SO and AAI', service.name)

        res = True
        for value in service_dict.values():
            res = res and value
            logger.info('####################### res is:%s, value is:%s', str(res), str(value))
        return res
