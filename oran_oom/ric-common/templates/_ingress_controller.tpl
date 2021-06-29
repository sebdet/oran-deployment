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

{{- define "common.ingresscontroller.url.platform" -}}
  {{- $keylist := list "common" "ingresscontroller" "url" "platform" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $url := include "locate" $ctx -}}
  {{- if not (empty $url) -}}
    {{- $url -}}
  {{- else -}}
    {{- printf "ric-entry" -}}
  {{- end -}}
{{- end -}}

{{- define "common.ingresscontroller.url.aux" -}}
  {{- $keylist := list "common" "ingresscontroller" "url" "aux" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $url := include "locate" $ctx -}}
  {{- if not (empty $url) -}}
    {{- $url -}}
  {{- else -}}
    {{- printf "aux-entry" -}}
  {{- end -}}
{{- end -}}


{{- define "common.ingresscontroller.url.dashboard" -}}
  {{- $keylist := list "common" "ingresscontroller" "url" "dashboard" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $url := include "locate" $ctx -}}
  {{- if not (empty $url) -}}
    {{- $url -}}
  {{- else -}}
    {{- printf "dashboard-entry" -}}
  {{- end -}}
{{- end -}}

{{- define "common.ingresscontroller.port.http" -}}
  {{- $keylist := list "common" "ingresscontroller" "port" "http" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $port := include "locate" $ctx -}}
  {{- if not (empty $port) -}}
    {{- $port -}}
  {{- else -}}
    {{- printf "32080" -}}
  {{- end -}}
{{- end -}}

{{- define "common.ingresscontroller.port.https" -}}
  {{- $keylist := list "common" "ingresscontroller" "port" "https" -}}
  {{- $ctx := dict "ctx" $.Values "keylist" $keylist -}}
  {{- $port := include "locate" $ctx -}}
  {{- if not (empty $port) -}}
    {{- $port -}}
  {{- else -}}
    {{- printf "32443" -}}
  {{- end -}}
{{- end -}}
