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

{{- define "common.name.a1mediator" -}}
  {{- printf "a1mediator" -}}
{{- end -}}

{{- define "common.fullname.a1mediator" -}}
  {{- $name := ( include "common.name.a1mediator" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.a1mediator" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.a1mediator" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.a1mediator" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.a1mediator" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.a1mediator" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.kongpath.ric.a1mediator" -}}/a1mediator{{- end -}}

{{- define "common.servicename.a1mediator.rmr" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.a1mediator.http" -}}
  {{- $name := ( include "common.fullname.a1mediator" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.a1mediator.rmr.data" -}}4562{{- end -}}
{{- define "common.serviceport.a1mediator.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.a1mediator.http" -}}10000{{- end -}}
