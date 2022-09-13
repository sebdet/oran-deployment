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
