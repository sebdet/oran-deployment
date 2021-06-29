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

{{- define "common.name.xapp-onboarder" -}}
  {{- printf "xapp-onboarder" -}}
{{- end -}}

{{- define "common.fullname.xapp-onboarder" -}}
  {{- $name := ( include "common.name.xapp-onboarder" . ) -}}
  {{- $namespace := ( include "common.namespace.platform" . ) -}}
  {{- printf "%s-%s" $namespace $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.configmapname.xapp-onboarder" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "configmap-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.deploymentname.xapp-onboarder" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "deployment-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.containername.xapp-onboarder" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "container-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "common.containername.xapp-onboarder.chartmuseum" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "container-%s-chartmuseum" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceaccountname.xapp-onboarder" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "svcacct-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.ingressname.xapp-onboarder" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "ingress-%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.servicename.xapp-onboarder.server" -}}
  {{- $name := ( include "common.fullname.xapp-onboarder" . ) -}}
  {{- printf "service-%s-http" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "common.serviceport.xapp-onboarder.server" -}}8888{{- end -}}
{{- define "common.serviceport.xapp-onboarder.chartmuseum" -}}8080{{- end -}}

{{- define "common.kongpath.ric.xapp-onboarder" -}}/onboard{{- end -}}
{{- define "common.kongpath.ric.chartmuseum" -}}/helmrepo{{- end -}}
