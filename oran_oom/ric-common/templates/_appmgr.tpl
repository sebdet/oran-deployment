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

{{- define "common.name.appmgr" -}}
  {{- printf "appmgr" -}}
{{- end -}}


{{- define "common.fullname.appmgr" -}}
  {{- $name := ( include "common.name.appmgr" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.serviceaccountname.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.kongpath.ric.appmgr" -}}/appmgr{{- end -}}

{{- define "common.servicename.appmgr.rmr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "service-%s-rmr" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.appmgr.http" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.secretname.appmgr" -}}
  {{- $name := ( include "common.fullname.appmgr" . ) -}}
  {{- printf "secret-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.appmgr.rmr.data" -}}4560{{- end -}}
{{- define "common.serviceport.appmgr.rmr.route" -}}4561{{- end -}}
{{- define "common.serviceport.appmgr.http" -}}8080{{- end -}}

