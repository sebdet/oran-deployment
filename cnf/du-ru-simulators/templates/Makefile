CNF_PACKAGE_NAME ?= oran-du-ru-simulators
CNF_PACKAGE_FOLDER ?= cnf-package-temp

CBA_SOURCE_FOLDER ?= cba
CBA_PACKAGE_NAME ?= CBA

HELM_REPO ?= local

DU_SIMULATOR_PACKAGE ?= du-simulator
DU_SIMULATOR_VERSION ?= 1.0.0

RU_SIMULATOR_PACKAGE ?= ru-simulator
RU_SIMULATOR_VERSION ?= 1.0.0

TOPOLOGY_SERVER_PACKAGE ?= topology-server
TOPOLOGY_SERVER_VERSION ?= 1.0.0

all: cleanup create-cnf-package-directory create-cba-package prepare-cnf-package zip-cnf-package print-success

create-cnf-package-directory:
	mkdir $(CNF_PACKAGE_FOLDER)

prepare-cnf-package:
	cp $(CBA_SOURCE_FOLDER)/target/$(CBA_PACKAGE_NAME)*.zip $(CNF_PACKAGE_FOLDER)/$(CBA_PACKAGE_NAME).zip
	cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(DU_SIMULATOR_PACKAGE) --version $(DU_SIMULATOR_VERSION) && mv $(DU_SIMULATOR_PACKAGE)-$(DU_SIMULATOR_VERSION).tgz helm_du_simulator.tgz
	cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(RU_SIMULATOR_PACKAGE) --version $(RU_SIMULATOR_VERSION) && mv $(RU_SIMULATOR_PACKAGE)-$(RU_SIMULATOR_VERSION).tgz helm_ru_simulator.tgz
	cd $(CNF_PACKAGE_FOLDER) && helm fetch $(HELM_REPO)/$(TOPOLOGY_SERVER_PACKAGE) --version $(TOPOLOGY_SERVER_VERSION) &&  mv $(TOPOLOGY_SERVER_PACKAGE)-$(TOPOLOGY_SERVER_VERSION).tgz helm_topology_server.tgz
	cp $(CBA_SOURCE_FOLDER)/MANIFEST.json $(CNF_PACKAGE_FOLDER)

zip-cnf-package:
	cd $(CNF_PACKAGE_FOLDER) && zip $(CNF_PACKAGE_NAME).zip * && mv $(CNF_PACKAGE_NAME).zip ..

print-success:
	echo "############ Package $(CNF_PACKAGE_NAME).zip BUILT SUCCESSFULLY !!! ################"

create-cba-package:
	cd $(CBA_SOURCE_FOLDER) && mvn --settings ../maven/settings.xml clean install

cleanup:
	rm -rf $(CNF_PACKAGE_FOLDER)
	rm -rf $(CNF_PACKAGE_NAME).zip
