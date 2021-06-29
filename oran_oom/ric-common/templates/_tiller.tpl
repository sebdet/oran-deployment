################################################################################
#   Copyright (c) 2019 AT&T Intellectual Property.                             #
#   Copyright (c) 2019 Nokia.                                                  #
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

{{- define "recursiveprinter" -}}
  {{- $ctx := .ctx }}
  {{- $printkeys := .printkeys }}
  {{- $currentkey := first $printkeys -}}
  {{- $restkeys := rest $printkeys -}}
  {{- if empty $restkeys -}}
    {{- $result := index $ctx $currentkey -}}
    {{- if not (empty $result) -}}
      {{- $result -}}
    {{- end -}}
  {{- else -}}
    {{- with index $ctx $currentkey }}
      {{- $newctx := dict "ctx" . "printkeys" $restkeys -}} 
      {{- include "recursiveprinter" $newctx -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{- define "printer" -}}
  {{- $topctx := .ctx }}
  {{- if hasKey $topctx.Values "common" }}
    {{- if hasKey $topctx.Values.common "tillers" }}
      {{- $ctx := index $topctx.Values.common.tillers .key -}}
      {{- if not (empty $ctx) -}}
        {{- $newctx := dict "ctx" $ctx "printkeys" .printkey -}}     
        {{- include "recursiveprinter" $newctx -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}




{{- define "common.tillerName" -}}
  {{- $printkey := list "name" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default "tiller-deploy" (include "printer" $newctx) -}}
{{- end -}}


{{- define "common.tillerNameSpace" -}}
  {{- $printkey := list "nameSpace" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default "kube-system" (include "printer" $newctx) -}}
{{- end -}}

{{- define "common.tillerDeployNameSpace" -}}
  {{- $printkey := list "deployNameSpace" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default "kube-system" (include "printer" $newctx) -}}
{{- end -}}



{{- define "common.tillerPort" -}}
  {{- $printkey := list "port" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default 44134 (include "printer" $newctx) -}}
{{- end -}}




{{- define "common.tillerTLSVerify" -}}
  {{- $printkey := list "tls" "verify" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default false (include "printer" $newctx) -}}
{{- end -}}


{{- define "common.tillerTLSAuthenticate" -}}
  {{- $printkey := list "tls" "authenticate" -}}
  {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
  {{- default false (include "printer" $newctx) -}}
{{- end -}}


{{- define "common.tillerHelmClientTLSSecret" -}}
  {{- $tlsverify := include "common.tillerTLSVerify" . }}
  {{- $tlsauthenticate := include "common.tillerTLSAuthenticate" . }}
  {{- if or (eq $tlsverify "true") (eq $tlsauthenticate "true") }}
    {{- $printkey := list "secret" "helmSecretName" -}}
    {{- $newctx := dict "ctx" .ctx "key" .key "printkey" $printkey }}
    {{- default "" (include "printer" $newctx) -}}
  {{- else -}}
    {{- printf "" -}}
  {{- end }}
{{- end -}}


{{- define "common.serviceaccountname.tiller" -}}
  {{- $name := ( include "common.tillerName" . ) -}}
  {{- printf "svcacct-tiller-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{- define "common.deploymentname.tiller" -}}
  {{- $name := ( include "common.tillerName" . ) -}}
  {{- printf "deployment-tiller-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "common.servicename.tiller" -}}
  {{- $topctx := .ctx }}
  {{- if hasKey $topctx.Values "common" }}
    {{- if hasKey $topctx.Values.common "tillers" }}
      {{- $ctx := index $topctx.Values.common.tillers .key -}}
      {{- if not (empty $ctx) -}}
        {{- if hasKey $ctx "name" -}}
          {{- $name := include "common.tillerName" . -}}
          {{- printf "service-tiller-%s" $name | trunc 63 | trimSuffix "-" -}}
        {{- else -}}
          {{ "tiller-deploy" }}
        {{- end -}}
      {{- else -}}
        {{ "tiller-deploy" }}
      {{- end -}}
    {{- else -}}
      {{ "tiller-deploy" }}
    {{- end -}}
  {{- else -}}
    {{ "tiller-deploy" }}
  {{- end -}}
{{- end -}}

{{- define "common.tillerEndpoint" -}}
  {{- $servicename := ( include "common.servicename.tiller" . ) -}}
  {{- $deploynamespace :=  ( include "common.tillerDeployNameSpace" . ) -}}
  {{- printf "%s.%s" $servicename $deploynamespace -}}
{{- end -}}
