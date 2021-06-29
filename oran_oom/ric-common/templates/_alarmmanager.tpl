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

{{- define "common.name.alarmmanager" -}}
  {{- printf "alarmmanager" -}}
{{- end -}}

{{- define "common.fullname.alarmmanager" -}}
  {{- $name := ( include "common.name.alarmmanager" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "common.kongpath.ric.alarmmanager" -}}/alarmmanager{{- end -}}

{{- define "common.servicename.alarmmanager.rmr" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.alarmmanager.http" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.alarmmanager.rest" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "service-%s-rest" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.pvname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "pv-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.pvcname.alarmmanager" -}}
  {{- $name := ( include "common.fullname.alarmmanager" . ) -}}
  {{- printf "pvc-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.alarmmanager.rmr.data" -}}4560{{- end -}}
{{- define "common.serviceport.alarmmanager.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.alarmmanager.http" -}}8080{{- end -}}
{{- define "common.serviceport.alarmmanager.rest" -}}8088{{- end -}}
