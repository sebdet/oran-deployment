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
"""Onap AAI model module."""
from onapsdk.aai.service_design_and_creation import Model
from oransdk.utils.jinja import jinja_env

class AaiModel(Model):
    """Model resource class."""

    def create(self,
               model_name: str,
               model_version_id: str,
               invariant_id: str) -> None:
        """Create Model.

        Args:
            model_name (str): model name
            model_version_id (str): model version id

        """
        self.send_message(
            "PUT",
            "Create A&AI service",
            f"{self.base_url}{self.api_version}/service-design-and-creation/"
            f"models/model/{invariant_id}",
            data=jinja_env().get_template("aai_model_create.json.j2")
            .render(
                model_version=self.resource_version,
                model_name=model_name,
                version_id=model_version_id,
                model_invariant_id=invariant_id
            )
        )
