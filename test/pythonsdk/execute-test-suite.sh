#!/bin/bash

sudo apt-get install python3.8
sudo apt-get install python3-pip

pip install --user pipenv
pip install --user --upgrade pipenv

~/.local/bin/pipenv install
~/.local/bin/pipenv run tests
