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

{{- define "common.name.messagerouter" -}}
  {{- printf "messagerouter" -}}
{{- end -}}

{{- define "common.fullname.messagerouter" -}}
  {{- $name := ( include "common.name.messagerouter" . ) -}}
  {{- $namespace := ( include "common.namespace.aux" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.messagerouter" -}}
  {{- $name := ( include "common.fullname.messagerouter" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.messagerouter" -}}
  {{- $name := ( include "common.fullname.messagerouter" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.messagerouter" -}}
  {{- $name := ( include "common.fullname.messagerouter" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.messagerouter" -}}
  {{- $name := ( include "common.fullname.messagerouter" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.messagerouter.tcp" -}}
  {{- $name := ( include "common.fullname.messagerouter" . ) -}}
  {{- printf "service-%s-tcp" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.messagerouter.http" -}}3904{{- end -}}
{{- define "common.serviceport.messagerouter.https" -}}3905{{- end -}}
{{- define "common.serviceport.messagerouter.kafka" -}}9092{{- end -}}
{{- define "common.serviceport.messagerouter.zookeeper" -}}2181{{- end -}}

{{- define "common.servicename.messagerouter.http" -}}ricaux-messagerouter{{- end -}}

