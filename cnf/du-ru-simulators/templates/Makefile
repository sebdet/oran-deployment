CNF_PACKAGE_NAME ?= oran-du-ru-simulators
CNF_PACKAGE_FOLDER ?= cnf-package

CBA_SOURCE_FOLDER ?= cba
CBA_PACKAGE_NAME ?= ORAN-DU-RU-SIMULATORS_CBA

HELM_REPO ?= local

DU_SIMULATOR_PACKAGE ?= du-simulator
DU_SIMULATOR_VERSION ?= 1.0.0

RU_SIMULATOR_PACKAGE ?= ru-simulator
RU_SIMULATOR_VERSION ?= 1.0.0

TOPOLOGY_SERVER_PACKAGE ?= topology-server
TOPOLOGY_SERVER_VERSION ?= 1.0.0

all: cleanup create-cnf-package-directory create-cba_package create-cnf-package

create-cnf-package-directory:
	mkdir $(CNF_PACKAGE_FOLDER)

create-cnf-package:
	cp $(CBA_SOURCE_FOLDER)/target/$(CBA_PACKAGE_NAME).zip $(CNF_PACKAGE_FOLDER)/
	cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(DU_SIMULATOR_PACKAGE) --version $(DU_SIMULATOR_VERSION) && mv $(DU_SIMULATOR_PACKAGE)_$(DU_SIMULATOR_VERSION) helm_du_simulator.tgz
   	cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(RU_SIMULATOR_PACKAGE) --version $(RU_SIMULATOR_VERSION) && mv $(RU_SIMULATOR_PACKAGE)_$(RU_SIMULATOR_VERSION) helm_ru_simulator.tgz
        cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(TOPOLOGY_SERVER_PACKAGE) --version $(TOPOLOGY_SERVER_VERSION) &&  mv $(TOPOLOGY_SERVER_PACKAGE)_$(TOPOLOGY_SERVER_VERSION) helm_topology_server.tgz
	cp $(CBA_SOURCE_FOLDER)/MANIFEST.json $(CNF_PACKAGE_FOLDER)

create-cba-package:
	cd $(CBA_SOURCE_FOLDER) && mvn --settings maven/settings.xml clean install

cleanup:
	rm -rf $(CNF_PACKAGE_FOLDER)

