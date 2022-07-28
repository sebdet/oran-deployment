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
from onapsdk.sdc.properties import Input, Property, ParameterError, NestedInput
from onapsdk.sdc.service import Service
from oransdk.sdc.sdc import SdcTemplate


# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start SDC Preparation")

class SdcPreparation():
    """Can be used to prepare SDC for Network Slicing usecase option2."""

    @classmethod
    def prepare_sdc(cls):
        """Create SDC templates."""
        sdc = SdcTemplate()
        vendor = sdc.create_vendor('aaaa')
        sdc.create_vsp('test1', vendor)

        # 0.create custom categories
        #logger.info("####################### create custom categories")
        #sdc.create_service_category(['CST', 'ServiceProfile', 'AN SliceProfile', 'CN SliceProfile', 'TN SliceProfile',
        #                             'NST', 'TN BH NSST', 'TN Network Requirement', 'AN NF NSST', 'CN NSST', 'Allotted Resource'])


        #vf_tn_bh_ar = cls.create_tn_resources(sdc, vendor)
        #vf_embban_nf_ar = cls.create_an_resources(sdc, vendor)
        #vf_embbcn_external_ar = cls.create_cn_resources(sdc, vendor)
        #cls.create_nst(sdc, vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar)

        vf_slice_ar = cls.create_slice_ar(sdc, vendor)

        srv_slice_profile_an_o2 = cls.create_an_slice_profiles(sdc, vf_slice_ar)
        #srv_slice_profile_tn = cls.create_tn_slice_profiles(sdc, vf_slice_ar)
        #srv_slice_profile_cn = cls.create_cn_slice_profiles(sdc, vf_slice_ar)

        #srv_profile_o2 = cls.create_service_profile(sdc, vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2)
        #cls.create_cst(sdc, srv_profile_o2)

    @classmethod
    def create_tn_resources(cls, sdc, vendor) -> dict:
        """Create TN related resources."""
        # 1.Create TN_Network_Requirement Service
        logger.info("####################### create TN_Network_Requirement Service")
        props = [Property('ConnectionLink', 'string', value='{\\"get_input\\":\\"ConnectionLink\\"}'),
                 Property('jitter', 'string', value='10'),
                 Property('latency', 'integer', value=10),
                 Property('maxBandwith', 'integer', value=1000)]

        srv_tn_network = sdc.create_service('TN_Network_Requirement', 'TN Network Requirement', properties=props)

        # 2.Create TN_Network_Req_AR
        logger.info("####################### create TN_Network_Req_AR")
        vf = sdc.create_vf('TN_Network_Req_AR', 'Allotted Resource', 'Allotted Resource', vendor)
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

        srv_tn_bh = sdc.create_service('Tn_ONAP_internal_BH', 'TN BH NSST', vnfs=[vf], role='ONAP_internal',
                                       properties=props)

        # 6.Create Tn_BH_AR
        logger.info("####################### Create Tn_BH_AR")
        vf_tn_bh_ar = sdc.create_vf('Tn_BH_AR', 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_tn_bh_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_tn_bh.unique_uuid
                c.get_property('providing_service_uuid').value = srv_tn_bh.identifier
                c.get_property('providing_service_name').value = srv_tn_bh.name
                break
        sdc.onboard_vf(vf_tn_bh_ar)
        return vf_tn_bh_ar

    @classmethod
    def create_an_resources(cls, sdc, vendor) -> dict:
        """Create AN related resources."""
        # 4.Create EmbbAn_NF Service Template
        logger.info("####################### create EmbbAn_NF Service Template")
        props = [Property('anNSSCap', 'org.openecomp.datatypes.NSSCapabilities')]
        srv_embban_nf = sdc.create_service('EmbbAn_NF', 'AN NF NSST', role='huawei', service_type='embb', properties=props)

        # 7.Create EmbbAn_NF_AR
        logger.info("####################### create EmbbAn_NF_AR")
        vf_embban_nf_ar = sdc.create_vf('EmbbAn_NF_AR', 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_embban_nf_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_embban_nf.unique_uuid
                c.get_property('providing_service_uuid').value = srv_embban_nf.identifier
                c.get_property('providing_service_name').value = srv_embban_nf.name
                break
        sdc.onboard_vf(vf_embban_nf_ar)
        return vf_embban_nf_ar

    @classmethod
    def create_cn_resources(cls, sdc, vendor) -> dict:
        """Create CN related resources."""
        # 5.Create EmbbCn_External Service Template
        logger.info("####################### create EmbbCn_External Service Template")
        srv_embbcn = Service(name='EmbbCn_External',
                             category='CN NSST',
                             role='huawei',
                             service_type='embb',
                             properties=[Property('aname', 'org.openecomp.datatypes.NSSCapabilities',
                                                  value="[{\\\"latency\\\":20,\\\"maxNumberofUEs\\\":10000,\\\"resourceSharingLevel\\\":\\\"Shared\\\",\\\"sST\\\":\\\"eMBB\\\",\\\"activityFactor\\\":30,\\\"areaTrafficCapDL\\\":800,\\\"areaTrafficCapUL\\\":800}]")])

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

        # 8.EmbbCn_External_AR
        logger.info("####################### create EmbbCn_External_AR")
        vf_embbcn_external_ar = sdc.create_vf('EmbbCn_External_AR', 'Allotted Resource', 'Allotted Resource', vendor)
        for c in vf_embbcn_external_ar.components:
            if c.name == 'AllottedResource 0':
                c.get_property('providing_service_invariant_uuid').value = srv_embbcn.unique_uuid
                c.get_property('providing_service_uuid').value = srv_embbcn.identifier
                c.get_property('providing_service_name').value = srv_embbcn.name
                break
        sdc.onboard_vf(vf_embbcn_external_ar)
        return vf_embbcn_external_ar


    @classmethod
    def create_nst(cls, sdc, vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar) -> None:
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
        sdc.create_service('EmbbNst_O2',
                           'NST',
                           role='option2',
                           vnfs=[vf_embbcn_external_ar, vf_embban_nf_ar, vf_tn_bh_ar],
                           properties=props)

    @classmethod
    def create_slice_ar(cls, sdc, vendor) -> dict:
        """Create Slice AR."""
        # 10. create Slice_AR
        logger.info("####################### create Slice_AR")

        vfc = Vfc('AllottedResource')
        vf_slice_ar = Vf(name='Slice_AR', category='Allotted Resource', subcategory='Allotted Resource', vendor=vendor)
        vf_slice_ar.create()
        if vf_slice_ar.status == const.DRAFT:
            vf_slice_ar.add_resource(vfc)

        component_uid = None
        for c in vf_slice_ar.components:
            if c.name == 'AllottedResource 0':
                component_uid = c.actual_component_uid
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
        return vf_slice_ar

    @classmethod
    def create_an_slice_profiles(cls, sdc, vf_slice_ar) -> dict:
        """Create AN Slice profile."""
        # 11.Create SliceProfile_AN_O2 Service Template
        logger.info("####################### create SliceProfile_AN_O2 Service Template")
        #slice_profile = "[{\\\"activityFactor\\\":20,\\\"areaTrafficCapDL\\\":100,\\\"areaTrafficCapUL\\\":100,\\\"cSAvailabilityTarget\\\":\\\"test\\\",\\\"cSRealibilityMeanTime\\\":100}]"
        slice_profile = "[{\\\"activityFactor\\\":20}]"

        an_slice_profile = [Property('ipAddress', 'string', value='{\\"get_input\\":\\"ipAddress\\"}'),
                            Property('logicInterfaceId', 'string', value='{\\"get_input\\":\\"logicInterfaceId\\"}'),
                            Property('nextHopInfo', 'string', value='{\\"get_input\\":\\"nextHopInfo\\"}')]
        complex_property =  Property('anSP', 'org.openecomp.datatypes.SliceProfile', value=slice_profile)


        srv_slice_profile_an_o2 = sdc.create_service_1('SliceProfile_AN',
                                                       'AN SliceProfile',
                                                       properties=an_slice_profile,
                                                       complex_input=complex_property,
                                                       vnfs=[vf_slice_ar])
        return srv_slice_profile_an_o2

    @classmethod
    def create_tn_slice_profiles(cls, sdc, vf_slice_ar) -> dict:
        """Create TN Slice profile."""
        # 12.Create SliceProfile_TN Service Template
        logger.info('####################### create service SliceProfile_TN')
        tn_slice_profile = [Property('jitter', 'string', value='{\\"get_input\\":\\"jitter\\"}'),
                            Property('latency', 'integer', value='{\\"get_input\\":\\"latency\\"}'),
                            Property('pLMNIdList', 'string', value='{\\"get_input\\":\\"pLMNIdList\\"}'),
                            Property('sNSSAI', 'string', 'value={\\"get_input\\":\\"sNSSAI\\"}'),
                            Property('sST', 'integer', value='{\\"get_input\\":\\"sST\\"}'),
                            Property('maxBandwidth', 'integer', value='{\\"get_input\\":\\"maxBandwidth\\"}')]

        srv_slice_profile_tn = sdc.create_service_1('SliceProfile_TN',
                                                    'TN SliceProfile',
                                                    vnfs=[vf_slice_ar],
                                                    properties=tn_slice_profile)
        return srv_slice_profile_tn

    @classmethod
    def create_cn_slice_profiles(cls, sdc, vf_slice_ar) -> dict:
        """Create CN Slice profile."""
        # 13.Create SliceProfile_CN Service Template
        logger.info('####################### create slice SliceProfile_CN')
        cn_slice_profile = [Property('ipAddress', 'string', value='{\\"get_input\\":\\"ipAddress\\"}'),
                            Property('logicInterfaceId', 'string', value='{\\"get_input\\":\\"logicInterfaceId\\"}'),
                            Property('nextHopInfo', 'string', value='{\\"get_input\\":\\"nextHopInfo\\"}')]
        srv_slice_profile_cn = sdc.create_service_1('SliceProfile_CN',
                                                    'CN SliceProfile',
                                                    vnfs=[vf_slice_ar],
                                                    properties=cn_slice_profile)
        return srv_slice_profile_cn

    @classmethod
    def create_service_profile(cls, sdc, vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2) -> dict:
        """Create Slice profile."""
        # 14.Create ServiceProfile_O2 Service Template
        logger.info('####################### create service ServiceProfile O2')
        service_profile = '[{' \
                            '\\"resourceSharingLevel\\":{\\"get_input\\":\\"spProp_resourceSharingLevel\\"},' \
                            '\\"sNSSAI\\":{\\"get_input\\":\\"spProp_sNSSAI\\"},' \
                            '\\"coverageAreaTAList\\":{\\"get_input\\":\\"spProp_coverageAreaTAList\\"},' \
                            '\\"sST\\":{\\"get_input\\":\\"spProp_sST\\"},' \
                            '\\"dLThptPerUE\\":{\\"get_input\\":\\"spProp_dLThptPerUE\\"},' \
                            '\\"uEMobilityLevel\\":{\\"get_input\\":\\"spProp_uEMobilityLevel\\"},'\
                            '\\"latency\\":{\\"get_input\\":\\"spProp_latency\\"},' \
                            '\\"uLThptPerUE\\":{\\"get_input\\":\\"spProp_uLThptPerUE\\"},' \
                            '\\"maxNumberofUEs\\":{\\"get_input\\":\\"spProp_maxNumberofUEs\\"}' \
                            '}]'
        service_props = [Property('spProp', 'org.openecomp.datatypes.ServiceProfile', value=service_profile)]
        srv_profile_o2 = sdc.create_service_1('ServiceProfile_O2',
                                              'ServiceProfile',
                                              properties=service_props,
                                              vnfs=[vf_slice_ar, srv_slice_profile_cn, srv_slice_profile_tn, srv_slice_profile_an_o2],
                                              role='option2')
        return srv_profile_o2

    @classmethod
    def create_cst(cls, sdc, srv_profile_o2) -> dict:
        """Create CST."""
        # 15.Create CST_O2 Service Template
        logger.info('####################### create service CST O2')
        props = '[{' \
                         '\\"coverageAreaList\\":{\\"get_input\\":\\"csProp_coverageAreaList\\"},' \
                        '\\"expDataRateDL\\":{\\"get_input\\":\\"csProp_expDataRateDL\\"},' \
                        '\\"expDataRateUL\\":{\\"get_input\\":\\"csProp_expDataRateUL\\"},' \
                        '\\"latency\\":{\\"get_input\\":\\"csProp_latency\\"},' \
                        '\\"maxNumberofUEs\\":{\\"get_input\\":\\"csProp_maxNumberofEUs\\"},' \
                        '\\"resourceSharingLevel\\":{\\"get_input\\":\\"csProp_resourceSharingLevel\\"},' \
                        '\\"uEMobilityLevel\\":{\\"get_input\\":\\"csProp_uEMobilityLevel\\"},' \
                        '\\"useInterval\\":{\\"get_input\\":\\"csProp_useInterval\\"},' \
                '}]'
        srv = sdc.create_service_1('CST_O2',
                                   'CST',
                                   role='option2',
                                   service_type='embb',
                                   vnfs=[srv_profile_o2],
                                   properties=[Property('csProp', 'org.openecomp.datatypes.CSProperties', value=props)])
        return srv
