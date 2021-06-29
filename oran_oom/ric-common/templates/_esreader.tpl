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


{{- define "common.name.esreader" -}}
  {{- printf "esreader" -}}
{{- end -}}


{{- define "common.fullname.esreader" -}}
  {{- $name := ( include "common.name.esreader" . ) -}}
  {{- $namespace := ( include "common.namespace.infra" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{- define "common.deploymentname.esreader" -}}
  {{- $name := ( include "common.fullname.esreader" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.configmapname.esreader" -}}
  {{- $name := ( include "common.fullname.esreader" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.containername.esreader" -}}
  {{- $name := ( include "common.fullname.esreader" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.serviceport.esreader.http" -}}8080{{- end -}}

{{- define "common.pvname.esreader" -}}
  {{- $name := ( include "common.fullname.esreader" . ) -}}
  {{- printf "pv-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.pvcname.esreader" -}}
  {{- $name := ( include "common.fullname.esreader" . ) -}}
  {{- printf "pvc-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

