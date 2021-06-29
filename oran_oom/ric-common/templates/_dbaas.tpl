################################################################################
#   Copyright (c) 2020 AT&T Intellectual Property.                             #
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

{{- define "common.name.dbaas" -}}
  {{- printf "dbaas" -}}
{{- end -}}

{{- define "common.fullname.dbaas" -}}
  {{- $name := ( include "common.name.dbaas" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.dbaas" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.dbaas" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.statefulsetname.dbaas" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "statefulset-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.dbaas" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.dbaas" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.dbaas.tcp" -}}
  {{- $name := ( include "common.fullname.dbaas" . ) -}}
  {{- printf "service-%s-tcp" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.dbaas.redis" -}}6379{{- end -}}
{{- define "common.serviceport.dbaas.sentinel" -}}26379{{- end -}}
