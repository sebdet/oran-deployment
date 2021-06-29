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


{{- define "common.name.mrsub" -}}
  {{- printf "mrsub" -}}
{{- end -}}

{{- define "common.fullname.mrsub" -}}
  {{- $name := ( include "common.name.mrsub" . ) -}}
  {{- $namespace := ( include "common.namespace.aux" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{- define "common.deploymentname.mrsub" -}}
  {{- $name := ( include "common.fullname.mrsub" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.configmapname.mrsub" -}}
  {{- $name := ( include "common.fullname.mrsub" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.containername.mrsub" -}}
  {{- $name := ( include "common.fullname.mrsub" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.serviceport.mrsub.http" -}}8080{{- end -}}
