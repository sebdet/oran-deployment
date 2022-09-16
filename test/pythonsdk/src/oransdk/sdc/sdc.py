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
"""Onap Sdc module."""
from time import sleep
import onapsdk.constants as const
from onapsdk.configuration import settings
from onapsdk.exceptions import APIError, ResourceNotFound
from onapsdk.onap_service import OnapService as Onap
from onapsdk.sdc.properties import Input, NestedInput, ParameterError

from onapsdk.sdc.vf import Vf
from onapsdk.sdc.vsp import Vsp
from onapsdk.sdc.vfc import Vfc
from onapsdk.sdc.vendor import Vendor
from oransdk.sdc.category_management import OranServiceCategory
from oransdk.sdc.service import OranService

class SdcTemplate(Onap):
    """Onap Sdc Template class."""

    def healthcheck(self) -> dict:
        """Healchcheck SDC components.

        Returns:
            status of SDC components
        """
        status = self.send_message_json("GET",
                                        "SDC Healchcheck",
                                        f"{settings.SDC_FE_URL}/sdc1/feProxy/rest/healthCheck")

        return status

    def create_service_category(self, category_names) -> None:
        """Create service category by names.

        Args:
            category_names : The list of category names
        """
        for cn in category_names:
            self._logger.info('creating service category [%s]', cn)
            OranServiceCategory.create(name=cn)


    def create_vendor(self, vendor_name) -> dict:
        """Create Vendor by names.

        Args:
            vendor_name : The vendor names
        Returns:
            the vendor
        """
        vendor = Vendor(vendor_name)
        vendor.create()
        try:
            vendor.onboard()
        except APIError as e:
            self._logger.error("Exception during vendor onboarding: %s", e)
            raise e
        return vendor

    def create_vsp(self, name, vendor, onboard=False) -> dict:
        """Create vsp.

        Args:
            name : The vsp name
            vendor : The vendor name
            onboard : The onboard flag
        Returns:
            the vsp
        """
        self._logger.info("creating vsp: [%s:%s]", name, vendor)
        retry = 0
        done = False

        vsp = Vsp(name=name, vendor=vendor)
        if onboard:
            while not done:
                try:
                    vsp.create()
                    vsp.onboard()
                except ResourceNotFound as e:
                    self._logger.error("Failed to onboard %s : %s", name, e)
                    retry = retry + 1
                    if retry >= 5:
                        raise e
                except APIError as e:
                    self._logger.error("Exception during vsp onboarding: %s", e)
                    raise e
                else:
                    done = True
        return vsp


    def create_vf(self, name, category, subcategory, vendor, onboard=False) -> dict:
        """Create vf.

        Args:
            name : The vf name
            category :  The category name
            subcategory : The subcategory name
            vendor : The vendor name
            onboard : The onboard flag
        Returns:
            the vf
        """
        self._logger.error("create vf: [%s:%s]", name, category)

        vfc = Vfc('AllottedResource')  # seemd incorrect
        vf = Vf(name=name, category=category, subcategory=subcategory, vendor=vendor)
        self._logger.error("create vf 2: ")
        vf.create()
        if vf.status == const.DRAFT:
            vf.add_resource(vfc)
            self._logger.error("create vf 3:")
            if onboard:
                self.onboard_vf(vf)
        return vf


    def onboard_vf(self, vf) -> None:
        """Onboard the vf.

        Args:
            vf : The vf to onboard
        """
        retry = 0
        done = False
        to = 2

        while not done:
            try:
                vf.onboard()
            except ResourceNotFound as e:
                retry += 1
                if retry > 5:
                    raise e
                sleep(to)
                to = 2 * to + 1
            else:
                done = True
        self._logger.info("onboarded vf: [%s]", vf.name)


    def create_service(self, name, category, vnfs=None, properties=None, inputs=None, role=None, service_type=None) -> dict:
        """Create service.

        Args:
             name : The service name
             category :  The category name
             vnfs : The list of vnfs
             properties : the list of properties
             role : the role value
             service_type : the service type
        Returns:
             the created service
        """
        self._logger.info("create service: [%s:%s]", name, category)
        retry = 0
        done = False

        if vnfs is None:
            vnfs = []
        if properties is None:
            properties = []

        srvc = OranService(name=name, category=category, properties=properties, inputs=inputs, role=role, service_type=service_type)
        srvc.create()

        while not done:
            try:
                if srvc.status == const.DRAFT:
                    for vnf in vnfs:
                        srvc.add_resource(vnf)

                if srvc.status != const.DISTRIBUTED:
                    srvc.onboard()
            except ResourceNotFound as e:
                retry += 1
                if retry > 5:
                    raise e
            else:
                done = True

        return srvc

    def create_service_1(self, name, category, vnfs=None, properties=None, inputs=None, complex_input=None, role=None, service_type=None) -> dict:
        """Create slicing profile service.

        Args:
             name : The service name
             category :  The category name
             vnfs : The list of vnfs
             properties : the list of properties
             inputs : the list of inputs
             complex_input : the predefined property type, that should be declared as input
             role : the role value
             service_type : the service type
        Returns:
             the created service
        """
        self._logger.info("create service: [%s:%s]", name, category)
        retry = 0
        done = False

        if vnfs is None:
            vnfs = []
        if properties is None:
            properties = []

        srvc = OranService(name=name, category=category, inputs=inputs, complex_input=complex_input, properties=properties, role=role, service_type=service_type)
        srvc.create()

        while not done:
            try:
                if srvc.status == const.DRAFT:
                    for vnf in vnfs:
                        srvc.add_resource(vnf)
                        for c in srvc.components:
                            self.set_property_input_slice_ar(vnf, srvc, c)

                if srvc.status != const.DISTRIBUTED:
                    srvc.onboard()
            except ResourceNotFound as e:
                retry += 1
                if retry > 5:
                    raise e
            else:
                done = True

        return srvc

    def set_property_input_slice_ar(self, vnf, service, component) -> None:
        """Get component property.

        Args:
            vnf: The vnf of the input
            service : The service
            component :  The component
        """
        self._logger.info("set property input slice ar: %s", component.name)
        if component.name.startswith("Slice_AR"):
            self._logger.info("get component Slice_AR 0")
            cp = self.get_component_property(component, 'allottedresource0_providing_service_invariant_uuid')
            if cp:
                self._logger.info('setting value on property [%s]', cp)
                service.declare_input(NestedInput(sdc_resource=vnf, input_obj=Input(unique_id="123",
                                                                                    input_type=cp.property_type,
                                                                                    name=cp.name,
                                                                                    sdc_resource=vnf)))
            else:
                raise ParameterError('no property providing_service_invariant_uuid found')

            cp = self.get_component_property(component, 'allottedresource0_providing_service_uuid')
            if cp:
                service.declare_input(NestedInput(sdc_resource=vnf, input_obj=Input(unique_id="123",
                                                                                    input_type=cp.property_type,
                                                                                    name=cp.name,
                                                                                    sdc_resource=vnf)))
            else:
                raise ParameterError('no property providing_service_uuid found')

    def get_component_property(self, component, name) -> dict:
        """Get component property.

        Args:
             component : The component
             name :  The property name
        Returns:
             the property
        """
        prop = None
        try:
            prop = list(filter(lambda x: x.name == name, component.properties))
            if prop:
                prop = prop[0]
            else:
                raise ParameterError('no property found')
        except ParameterError as e:
            self._logger.error("component [%s] has no property [%s]", component.name, name)
            raise e

        self._logger.error("retrived property [%s] for component [%s]", prop.name if prop else 'null', component.name)
        return prop
