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

{{- define "common.name.dashboard" -}}
  {{- printf "dashboard" -}}
{{- end -}}


{{- define "common.fullname.dashboard" -}}
  {{- $name := ( include "common.name.dashboard" . ) -}}
  {{- $namespace := ( include "common.namespace.aux" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.dashboard" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.dashboard" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.dashboard" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.dashboard" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.dashboard" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.dashboard.http" -}}
  {{- $name := ( include "common.fullname.dashboard" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.dashboard.http" -}}30080{{- end -}}
{{- define "common.serviceport.dashboard.container" -}}8080{{- end -}}
