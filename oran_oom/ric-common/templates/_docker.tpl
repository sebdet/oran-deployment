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

{{- define "common.dockerregistry.url" -}}
  {{- $defaultregistry := .defaultregistry }}
  {{- $keylist := list $.ctx.Chart.Name "registry" -}}
  {{- $ctx := dict "ctx" $.ctx.Values "keylist" $keylist -}}
  {{- $overrideregistry := include "locate" $ctx -}}
  {{- $keylist := list "common" "localregistry" -}}
  {{- $ctx := dict "ctx" $.ctx.Values "keylist" $keylist -}}
  {{- $localregistry := include "locate" $ctx -}}
  {{- if not (empty $overrideregistry) -}}
    {{- $overrideregistry -}}
  {{- else -}}
    {{- if not (empty $localregistry) -}}
      {{- $localregistry -}}
    {{- else -}}
      {{- $defaultregistry -}}
    {{- end -}}
  {{- end -}}
{{- end -}}


{{- define "common.dockerregistry.credential" -}}
  {{- $reponame := include "common.dockerregistry.url" . -}}
  {{- $postfix := $reponame | replace "." "-" | replace ":" "-" | replace "/" "-" | trunc 63 | trimSuffix "-" -}}
  {{- printf "secret-%s" $postfix -}}
{{- end -}}


{{- define "common.dockerregistry.pullpolicy" -}}
  {{- $defaulpullpolicy := .defaultpullpolicy }}
  {{- $keylist := list $.ctx.Chart.Name "pullpolicy" -}}
  {{- $ctx := dict "ctx" $.ctx.Values "keylist" $keylist -}}
  {{- $overridepullpolicy := include "locate" $ctx -}}
  {{- $keylist := list "common" "pullpolicy" -}}
  {{- $ctx := dict "ctx" $.ctx.Values "keylist" $keylist -}}
  {{- $globalpullpolicy := include "locate" $ctx -}}
  {{- if not (empty $overridepullpolicy) -}}
    {{- $overridepullpolicy -}}
  {{- else -}}
    {{- if not (empty $globalpullpolicy) -}}
      {{- $globalpullpolicy -}}
    {{- else -}}
      {{- $defaulpullpolicy -}}
    {{- end -}}
  {{- end -}}
{{- end -}}


