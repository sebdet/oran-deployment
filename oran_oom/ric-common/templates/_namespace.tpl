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

{{- define "common.namespace.platform" -}}
  {{- $keylist := list "common" "namespace" "platform" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $namespace := include "locate" $ctx -}}
  {{- if not (empty $namespace) -}}
    {{- $namespace -}}
  {{- else -}}
    {{- printf "ricplt" -}}
  {{- end -}}
{{- end -}}

{{- define "common.namespace.infra" -}}
  {{- $keylist := list "common" "namespace" "infra" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $namespace := include "locate" $ctx -}}
  {{- if not (empty $namespace) -}}
    {{- $namespace -}}
  {{- else -}}
    {{- printf "ricinfra" -}}
  {{- end -}}
{{- end -}}

{{- define "common.namespace.xapp" -}}
  {{- $keylist := list "common" "namespace" "xapp" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $namespace := include "locate" $ctx -}}
  {{- if not (empty $namespace) -}}
    {{- $namespace -}}
  {{- else -}}
    {{- printf "ricxapp" -}}
  {{- end -}}
{{- end -}}


{{- define "common.namespace.aux" -}}
  {{- $keylist := list "common" "namespace" "aux" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $namespace := include "locate" $ctx -}}
  {{- if not (empty $namespace) -}}
    {{- $namespace -}}
  {{- else -}}
    {{- printf "ricaux" -}}
  {{- end -}}
{{- end -}}
