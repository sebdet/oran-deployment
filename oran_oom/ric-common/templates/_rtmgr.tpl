################################################################################
#   Copyright (c) 2019 AT&T Intellectual Property.                             #
#                                                                              #
#   Licensed under the Apache License, Version 2.0 (the "License");            #
#   you may not use this file except in compliance with the License.           #
#   You may obtain a copy of the License at                                    #
#                                                                              #
#       http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                              #
#   Unless required by applicable law or agreed to in writing, software        #
#   distributed under the License is distributed on an "AS IS" BASIS,          #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#   See the License for the specific language governing permissions and        #
#   limitations under the License.                                             #
################################################################################

{{- define "common.name.rtmgr" -}}
  {{- printf "rtmgr" -}}
{{- end -}}

{{- define "common.fullname.rtmgr" -}}
  {{- $name := ( include "common.name.rtmgr" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.rtmgr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.rtmgr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.rtmgr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.rtmgr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.rtmgr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.rtmgr.rmr" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.rtmgr.http" -}}
  {{- $name := ( include "common.fullname.rtmgr" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.rtmgr.rmr.data" -}}4560{{- end -}}
{{- define "common.serviceport.rtmgr.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.rtmgr.http" -}}3800{{- end -}}
