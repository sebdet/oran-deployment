#!/usr/bin/env python3
###
# ============LICENSE_START=======================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
# Copyright (C) 2022 AT&T Intellectual Property. All rights
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
"""SDC Service module."""

from typing import Dict, Iterator, List, Optional, Union
from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc.component import Component
from onapsdk.sdc.properties import Property, NestedInput
from onapsdk.sdc.service import Service, ServiceInstantiationType
from onapsdk.sdc.sdc_resource import SdcResource
from onapsdk.utils.headers_creator import headers_sdc_creator
from oransdk.utils.jinja import jinja_env


class OranService(Service):  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """ONAP Service Object used for SDC operations."""

    def __init__(self, name: str = None, version: str = None, sdc_values: Dict[str, str] = None,  # pylint: disable=too-many-arguments
                 resources: List[SdcResource] = None, properties: List[Property] = None, complex_input: Property = None,
                 inputs: List[Union[Property, NestedInput]] = None,
                 instantiation_type: Optional[ServiceInstantiationType] = \
                     None,
                 category: str = None, role: str = "", function: str = "", service_type: str = ""):
        """
        Initialize service object.

        Args:
            name (str, optional): the name of the service
            version (str, optional): the version of the service
            sdc_values (Dict[str, str], optional): dictionary of values
                returned by SDC
            resources (List[SdcResource], optional): list of SDC resources
            properties (List[Property], optional): list of properties to add to service.
                None by default.
            inputs (List[Union[Property, NestedInput]], optional): list of inputs
                to declare for service. It can be both Property or NestedInput object.
                None by default.
            instantiation_type (ServiceInstantiationType, optional): service instantiation
                type. ServiceInstantiationType.A_LA_CARTE by default
            category (str, optional): service category name
            role (str, optional): service role
            function (str, optional): service function. Empty by default
            service_type (str, optional): service type. Empty by default
            complex_input (List[Property], optional): internal defined property type, that needs to be declared as input.
                None by default.

        """
        super().__init__(name=name, sdc_values=sdc_values, version=version, properties=properties,
                         inputs=inputs, category=category, resources=resources,
                         instantiation_type=instantiation_type, role=role, function=function, service_type=service_type)
        self.complex_input = complex_input

    @property
    def components(self) -> Iterator[Component]:
        """Resource components.

        Iterate resource components.

        Yields:
            Component: Resource component object

        """
        for component_instance in self.send_message_json(\
                "GET",
                f"Get {self.name} resource inputs",
                f"{self.resource_inputs_url}/filteredDataByParams?include=componentInstances"
                ).get("componentInstances", []):
            sdc_resource: "SdcResource" = None

            if component_instance['originType'] == "ServiceProxy":
                sdc_resource = SdcResource.import_from_sdc(self.send_message_json(\
                            "GET",
                            f"Get {self.name} component's SDC resource metadata",
                            (f"{self.base_front_url}/sdc1/feProxy/rest/v1/catalog/services/"
                             f"{component_instance['actualComponentUid']}/"
                             "filteredDataByParams?include=metadata"))["metadata"])
            else:
                sdc_resource = SdcResource.import_from_sdc(self.send_message_json(\
                    "GET",
                    f"Get {self.name} component's SDC resource metadata",
                    (f"{self.base_front_url}/sdc1/feProxy/rest/v1/catalog/resources/"
                     f"{component_instance['actualComponentUid']}/"
                     "filteredDataByParams?include=metadata"))["metadata"])

            yield Component.create_from_api_response(api_response=component_instance,
                                                     sdc_resource=sdc_resource,
                                                     parent_sdc_resource=self)

    def declare_complex_input(self, property_obj: Property) -> None:
        """Declare complex input for resource's property.

        For each property input can be declared.

        Args:
            property_obj (Property): Property to declare input

        """
        self._logger.debug("Declare input for Complex property")
        if property_obj.property_type == "org.openecomp.datatypes.SliceProfile":
            self._logger.debug("Declare input for SliceProfile")
            self.send_message_json("POST",
                                   f"Declare new input for {property_obj.name} property",
                                   f"{self.resource_inputs_url}/create/inputs",
                                   data=jinja_env().get_template(\
                                   "sdc_add_slice_profile_input.json.j2").\
                                       render(\
                                           sdc_resource=self,
                                           property=property_obj))
        elif property_obj.property_type == "org.openecomp.datatypes.ServiceProfile":
            self._logger.debug("Declare input for ServiceProfile")
            self.send_message_json("POST",
                                   f"Declare new input for {property_obj.name} property",
                                   f"{self.resource_inputs_url}/create/inputs",
                                   data=jinja_env().get_template(\
                                       "sdc_add_service_profile_input.json.j2").\
                                           render(\
                                               sdc_resource=self,
                                               property=property_obj))
        elif property_obj.property_type == "org.openecomp.datatypes.CSProperties":
            self._logger.debug("Declare input for CSProperties")
            self.send_message_json("POST",
                                   f"Declare new input for {property_obj.name} property",
                                   f"{self.resource_inputs_url}/create/inputs",
                                   data=jinja_env().get_template(\
                                       "sdc_add_cs_properties_input.json.j2").\
                                            render(\
                                                sdc_resource=self,
                                                property=property_obj))
        else:
            self._logger.error("Data type %s not supported", property_obj.property_type)

    def declare_resource_input(self,
                               input_to_declare: Property) -> None:
        """Declare input for given property, nested input or component property object.

        Call SDC FE API to declare input for given property.

        Args:
            input_declaration (Union[Property, NestedInput]): Property or ComponentProperty
                to declare input or NestedInput object

        Raises:
            ParameterError: if the given property is not SDC resource property

        """
        self.send_message("POST",
                          f"Declare new input for {input_to_declare.name} property",
                          f"{self.resource_inputs_url}/create/inputs",
                          data=jinja_env().get_template(\
                              "component_declare_input.json.j2").\
                                  render(\
                                      component=input_to_declare.component,
                                      property=input_to_declare))

    def declare_resources_and_properties(self) -> None:
        """Delcare resources and properties.

        It declares also inputs.

        """
        for resource in self.resources:
            self.add_resource(resource)
        for property_to_add in self._properties_to_add:
            self.add_property(property_to_add)
        for input_to_add in self._inputs_to_add:
            self.declare_input(input_to_add)
        if self.complex_input is not None:
            self.declare_complex_input(self.complex_input)


    def get_distribution_status(self) -> dict:
        """Get service distribution status."""
        url = "{}/services/distribution/{}".format(self._base_create_url(),
                                                   self.distribution_id)
        headers = headers_sdc_creator(SdcResource.headers)
        try:
            result = self.send_message_json("GET",
                                            "Check distribution for {}".format(
                                                self.name),
                                            url,
                                            headers=headers)
        except ResourceNotFound:
            msg = f"No distributions found for {self.name} of {self.__class__.__name__}."
            self._logger.debug(msg)
        else:
            return result
