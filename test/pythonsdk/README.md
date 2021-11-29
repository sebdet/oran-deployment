# Python ORAN SDK

an extension of ONAP SDK, to use ORAN and ONAP components programmatically with Python code


## Description

ORAN SDK is an extension of ONAP SDK. Please check [doc](https://python-onapsdk.readthedocs.io/en/latest/index.html) site to find out all the features about ONAP SDK.

This project aims to provide a consistent and complete set of interactions with ORAN’s many services.

Using few python commands, you should be able to run different tests with different components from ONAP and ORAN.

## Development

Before you start, ensure you have Python installation in version 3.8.
Please see [the official Python documentation](https://docs.python.org/3/using/index.html) 
in case you have to upgrade or install certain Python version.

### Setting up development environment

Clone the project. Inside the project folder create a new virtual environment:

```
$ python -m venv <project_home>/test/pythonsdk/env
```
or
```
$ python3.8 -m venv <project_home>/test/pythonsdk/env
```
Then activate the virtual environment:
```
$ source <project_home>/test/pythonsdk/env/bin/activate
```
On Windows, activate by executing the following:

```
$ .<project_home>\test\pythonsdk\env\Scripts\activate
```

### Developing
To use ONAP SDK library functions, install the onapsdk lib first:

```
$ pip install onapsdk
```

To use library functions directly from the ORAN SDK source code, execute the following
to point to the source folder in *PYTHONPATH* variable and run the interpreter:

```
$ PYTHONPATH=$PYTHONPATH:<project_home>/test/pythonsdk/src/ python
```

On Windows:

```
$ $env:PYTHONPATH='<project_home>\test\pythonsdk\src\';python
```

You can then start working with library functions from both ONAP SDK and ORAN SDK as needed.

### Testing

This project uses tox to run all the tests and do lint and docstyle checks.

To execute the texts, please install first [tox](https://tox.readthedocs.io/en/latest/index.html):

```
$ pip install tox
```


#### Unit testing
To run all the unit test:

```
$ tox -e unit-tests
```

#### Integration testing

To run the integration tests, start all the needed ONAP and ORAN components first with kubernetes.

Go to *scripts/layer-2* directory and start all the needed components with the scripts.

When all the components are started, update *pythonsdk/src/orantests/configuration/settings.py* with the correct URLs for all the components.

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