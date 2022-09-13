#!/usr/bin/env python3
###
# ============LICENSE_START===================================================
# ORAN SMO PACKAGE - PYTHONSDK TESTS
# ================================================================================
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
"""Prepare OOF for Network Slicing option2 test."""
import os
import logging
import logging.config
import subprocess
import sys
from subprocess import check_output
from onapsdk.configuration import settings
from oransdk.policy.policy import OranPolicy

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("####################### Start OOF Preparation")

# Set working dir as python script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class OofPreparation():
    """Can be used to prepare OOF for Network Slicing usecase option2."""

    @classmethod
    def prepare_oof(cls, nst_name, an_nsst_name, tn_nsst_name):
        """Prepare OOF, create optimization policies."""
        # copy policy creation package to oof pod
        logger.info("####################### copy policy generation package to OOF pod:%s", dname)
        oof_pod = subprocess.run("kubectl get pods -n onap | awk '{print $1}' | grep  onap-oof-[a-z0-9]*-[a-z0-9]*$", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        cmd = f"kubectl cp ../resources/policies_option2.tar.gz -n onap {oof_pod}:/opt/osdf"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- tar -xvf policies_option2.tar.gz"
        check_output(cmd, shell=True).decode('utf-8')

        # run python command to create policies
        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py create_policy_types policy_types"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py create_and_push_policies nst_policies"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py generate_nsi_policies {nst_name}"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py create_and_push_policies gen_nsi_policies"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py generate_nssi_policies {an_nsst_name} minimize latency"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py create_and_push_policies gen_nssi_policies"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py generate_nssi_policies {tn_nsst_name}  minimize latency"
        check_output(cmd, shell=True).decode('utf-8')

        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py create_and_push_policies gen_nssi_policies"
        check_output(cmd, shell=True).decode('utf-8')

        #Verify policies created
        policy = OranPolicy()
        policy_status_list = policy.get_policy_status(settings.POLICY_BASICAUTH)
        if len(policy_status_list) != 20:
            logger.info("####################### Policy created failed. 20 policies expected, but only %s found. Please verify manually.", str(len(policy_status_list)))
            sys.exit('OOF preparation failed. Exception while creating policies. Please check the policies manually.')

    @classmethod
    def cleanup_oof(cls):
        """Delete OOF optimization policies."""
        oof_pod = subprocess.run("kubectl get pods -n onap | awk '{print $1}' | grep  onap-oof-[a-z0-9]*-[a-z0-9]*$", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

        # run python command to create policies
        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py delete_policies nst_policies"
        check_output(cmd, shell=True).decode('utf-8')

        #python3 policy_utils.py create_and_push_policies gen_nsi_policies
        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py delete_policies gen_nsi_policies"
        check_output(cmd, shell=True).decode('utf-8')

        #python3 policy_utils.py create_and_push_policies gen_nssi_policies
        cmd = f"kubectl exec -ti -n onap {oof_pod} -- python3 policies_option2/policy_utils.py delete_policies gen_nssi_policies"
        check_output(cmd, shell=True).decode('utf-8')

        # run python command to create policies
        logger.info("####################### copy policy generation package to OOF pod:%s", dname)
        cmd = f"kubectl exec -ti -n onap {oof_pod} -- rm -rf policies_option2"
        check_output(cmd, shell=True).decode('utf-8')
