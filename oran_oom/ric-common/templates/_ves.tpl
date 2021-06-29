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

{{- define "common.name.ves" -}}
  {{- printf "ves" -}}
{{- end -}}


{{- define "common.fullname.ves" -}}
  {{- $name := ( include "common.name.ves" . ) -}}
  {{- $namespace := ( include "common.namespace.aux" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.ves" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.ves" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.ves" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.ves" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.ves" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.kongpath.aux.vescollector" -}}/vescollector{{- end -}}

{{- define "common.servicename.ves.http" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.ves.tcp" -}}
  {{- $name := ( include "common.fullname.ves" . ) -}}
  {{- printf "service-%s-tcp" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.ves.http" -}}8080{{- end -}}
{{- define "common.serviceport.ves.https" -}}8443{{- end -}}
