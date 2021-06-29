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

{{- define "common.name.rsm" -}}
  {{- printf "rsm" -}}
{{- end -}}

{{- define "common.fullname.rsm" -}}
  {{- $name := ( include "common.name.rsm" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.rsm" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.rsm" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.rsm" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.rsm" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.rsm" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.kongpath.ric.rsm" -}}/rsm{{- end -}}

{{- define "common.servicename.rsm.rmr" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.rsm.http" -}}
  {{- $name := ( include "common.fullname.rsm" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.rsm.rmr.data" -}}4801{{- end -}}
{{- define "common.serviceport.rsm.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.rsm.http" -}}4800{{- end -}}
