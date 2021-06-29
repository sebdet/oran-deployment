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

{{- define "common.name.e2mgr" -}}
  {{- printf "e2mgr" -}}
{{- end -}}

{{- define "common.fullname.e2mgr" -}}
  {{- $name := ( include "common.name.e2mgr" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.e2mgr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.e2mgr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.e2mgr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.e2mgr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.e2mgr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.kongpath.ric.e2mgr" -}}/e2mgr{{- end -}}

{{- define "common.servicename.e2mgr.rmr" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.e2mgr.http" -}}
  {{- $name := ( include "common.fullname.e2mgr" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.e2mgr.rmr.data" -}}3801{{- end -}}
{{- define "common.serviceport.e2mgr.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.e2mgr.http" -}}3800{{- end -}}
