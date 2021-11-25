#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`pwd`/src 
export ONAP_PYTHON_SDK_SETTINGS=orantests.configuration.settings 

pytest --junit-xml=oran-tests.xml
