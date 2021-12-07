# Python ORAN SDK

An extension of ONAP SDK, to use ORAN and ONAP components programmatically with Python code

## Description

ORAN SDK is an extension of ONAP SDK. Please check [doc](https://python-onapsdk.readthedocs.io/en/latest/index.html) site to find out all the features about ONAP SDK.

This project aims to provide a consistent and complete set of interactions with ORAN’s many services.

Using few python commands, you should be able to run different tests with different components from ONAP and ORAN.

### Setting up development environment

Ensure you have executed the script located in ... scripts/layer-0/0-setup-tests-env.sh
This will setup eveything for you.

### Testing

This project uses tox to run all the tests and do lint and docstyle checks.

```
$ tox
```

#### Unit testing
To run only the unit test:

```
$ tox -e unit-tests
```

#### Integration testing

To run the integration tests, start all the needed ONAP and ORAN components & network simulators first on kubernetes.

Go to *scripts/layer-2* directory and start all the needed components with the scripts.

Then execute the integration tests with command:

```
$ tox -e oran-tests
```

#### Code analyse and check style checking
To run code analyse and check check styles:

```
$ tox -e pylint
```

To check compliance with Python docstring conventions:

```
$ tox -e pydocstyle
```
