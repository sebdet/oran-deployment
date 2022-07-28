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
"""Onap SDC Category Management module."""
import json
from onapsdk.sdc.category_management import ServiceCategory

class OranServiceCategory(ServiceCategory):
    """Onap SDC Category Management module ."""

    @classmethod
    def create(cls, name: str) -> "BaseCategory":
        """Create category instance.

        Checks if category with given name exists and if it already
            exists just returns category with given name.

        Returns:
            BaseCategory: Created category instance

        """
        category_obj: "BaseCategory" = cls(name)
        if category_obj.exists():
            return category_obj
        cls.send_message_json("POST",
                              f"Create {name} {cls.category_name()}",
                              cls._base_create_url(),
                              data=json.dumps({"name": name, "models": ["SDC AID"], "metadataKeys": []}),
                              headers=cls.headers())
        category_obj.exists()
        return category_obj

    @classmethod
    def get(cls, name: str, subcategory: str = None) -> "ResourceCategory":  # pylint: disable=arguments-differ
        """Get resource category with given name.

        It returns resource category with all subcategories by default. You can
            get resource category with only one subcategory if you provide it's
            name as `subcategory` parameter.

        Args:
            name (str): Resource category name.
            subcategory (str, optional): Name of subcategory. Defaults to None.

        Raises:
            ResourceNotFound: Subcategory with given name does not exist

        Returns:
            BaseCategory: BaseCategory instance

        """
        self._logger.error("resource is ResourceCategory: %s:%s", name, subcategory)
        category_obj: "ResourceCategory" = super().get(name=name)
        if not subcategory:
            self._logger.error("No subcategory")
            return category_obj
        filtered_subcategories: Dict[str, str] = list(filter(lambda x: x["name"] == subcategory,
                                                             category_obj.subcategories))
        if not filtered_subcategories:
            self._logger.error("No filtered_subcategories")
            raise ResourceNotFound(f"Subcategory {subcategory} does not exist.")
        self._logger.error("category_obj: %s:%s", category_obj, filtered_subcategories)
        category_obj.subcategories = filtered_subcategories
        return category_obj
