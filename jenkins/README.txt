The ORAN SMO CI/CD is structured like this:
--> Helm chart deploys Jenkins.
    --> Contains Jobs, jenkins config in JCasC
	--> Jobs defined in Job DSL in JCasC
		--> They refer to github Pipelines written in Groovy Script.


Doc for jenkins:
----------------

Jenkins helm charts:
https://github.com/jenkinsci/helm-charts

Possible values for charts:
https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/values.yaml
https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/VALUES_SUMMARY.md

--> controller.JCasC.configScripts defines the advanced JCasC config (the one that can be exported in jenkins)
 Each yaml key will create a config file with the content specified below that key

JCasc config thruth (local):
https://192.168.1.46:32080/configuration-as-code

Job DSL schema thruth (local)
http://192.168.1.46:32080/plugin/job-dsl/api-viewer/index.html

