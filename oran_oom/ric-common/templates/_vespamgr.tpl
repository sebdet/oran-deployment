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

{{- define "common.name.vespamgr" -}}
  {{- printf "vespamgr" -}}
{{- end -}}

{{- define "common.fullname.vespamgr" -}}
  {{- $name := ( include "common.name.vespamgr" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.vespamgr" -}}
  {{- $name := ( include "common.fullname.vespamgr" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.vespamgr" -}}
  {{- $name := ( include "common.fullname.vespamgr" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.vespamgr" -}}
  {{- $name := ( include "common.fullname.vespamgr" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.vespamgr.http" -}}
  {{- $name := ( include "common.fullname.vespamgr" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.vespamgr.alert" -}}
  {{- $name := ( include "common.fullname.vespamgr" . ) -}}
  {{- printf "service-%s-alert" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.vespamgr.http" -}}8080{{- end -}}
{{- define "common.serviceport.vespamgr.alert" -}}9095{{- end -}}
