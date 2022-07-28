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

from typing import Iterator
import os
from onapsdk.sdc.component import Component
from onapsdk.sdc.properties import Property
from onapsdk.sdc.service import Service
from onapsdk.sdc.sdc_resource import SdcResource
from oransdk.utils.jinja import jinja_env


class OranService(Service):  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """ONAP Service Object used for SDC operations."""

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
        self._logger.debug("Declare input for SliceProfile property")
        self.send_message_json("POST",
                               f"Declare new input for {property_obj.name} property",
                               f"{self.resource_inputs_url}/create/inputs",
                               data=jinja_env().get_template(\
                                   "sdc_resource_add_complex_input.json.j2").\
                                       render(\
                                           sdc_resource=self,
                                           property=property_obj))

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