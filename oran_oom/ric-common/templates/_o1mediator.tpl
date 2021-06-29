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

{{- define "common.name.o1mediator" -}}
  {{- printf "o1mediator" -}}
{{- end -}}

{{- define "common.fullname.o1mediator" -}}
  {{- $name := ( include "common.name.o1mediator" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.o1mediator" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.o1mediator" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.o1mediator" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.o1mediator" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.o1mediator" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "common.kongpath.ric.o1mediator" -}}/o1mediator{{- end -}}

{{- define "common.servicename.o1mediator.http" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.o1mediator.tcp.netconf" -}}
  {{- $name := ( include "common.fullname.o1mediator" . ) -}}
  {{- printf "service-%s-tcp-netconf" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.serviceport.o1mediator.http.supervise" -}}9001{{- end -}}
{{- define "common.serviceport.o1mediator.http.mediation" -}}8080{{- end -}}
{{- define "common.serviceport.o1mediator.http.event" -}}3000{{- end -}}
{{- define "common.serviceport.o1mediator.tcp.netconf" -}}830{{- end -}}

{{- define "common.nodeport.o1mediator.tcp.netconf" -}}30830{{- end -}}
