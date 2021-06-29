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

{{- define "common.name.jaegeradapter" -}}
  {{- printf "jaegeradapter" -}}
{{- end -}}

{{- define "common.fullname.jaegeradapter" -}}
  {{- $name := ( include "common.name.jaegeradapter" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.jaegeradapter" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.jaegeradapter" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.jaegeradapter" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.servicename.jaegeradapter.query" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "service-%s-query" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "common.servicename.jaegeradapter.collector" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "service-%s-collector" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "common.servicename.jaegeradapter.agent" -}}
  {{- $name := ( include "common.fullname.jaegeradapter" . ) -}}
  {{- printf "service-%s-agent" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.jaegeradapter.zipkincompact" -}}5775{{- end -}}
{{- define "common.serviceport.jaegeradapter.jaegercompact" -}}6831{{- end -}}
{{- define "common.serviceport.jaegeradapter.jaegerbinary" -}}6832{{- end -}}
{{- define "common.serviceport.jaegeradapter.httpquery" -}}16686{{- end -}}
{{- define "common.serviceport.jaegeradapter.httpconfig" -}}5778{{- end -}}
{{- define "common.serviceport.jaegeradapter.zipkinhttp" -}}9411{{- end -}}
{{- define "common.serviceport.jaegeradapter.jaegerhttp" -}}14268{{- end -}}
{{- define "common.serviceport.jaegeradapter.jaegerhttpt" -}}14267{{- end -}}

{{- define "common.portname.jaegeradapter.zipkincompact" -}}"zipkincompact"{{- end -}}
{{- define "common.portname.jaegeradapter.jaegercompact" -}}"jaegercompact"{{- end -}}
{{- define "common.portname.jaegeradapter.jaegerbinary" -}}"jaegerbinary"{{- end -}}
{{- define "common.portname.jaegeradapter.zipkinhttp" -}}"zipkinhttp"{{- end -}}
{{- define "common.portname.jaegeradapter.jaegerhttp" -}}"jaegerhttp"{{- end -}}
{{- define "common.portname.jaegeradapter.jaegerhttpt" -}}"jaegerhttpt"{{- end -}}
{{- define "common.portname.jaegeradapter.httpquery" -}}"httpquery"{{- end -}}
{{- define "common.portname.jaegeradapter.httpconfig" -}}"httpconfig"{{- end -}}
