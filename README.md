# IPFabric

IPFabric is a Python module for connecting to and communicating against an IP Fabric instance.

## About

Founded in 2015, [IP Fabric](https://ipfabric.io/) develops network infrastructure visibility and analytics solution to
help enterprise network and security teams with network assurance and automation across multi-domain heterogeneous
environments. From in-depth discovery, through graph visualization, to packet walks and complete network history, IP
Fabric enables to confidently replace manual tasks necessary to handle growing network complexity driven by relentless
digital transformation.

## Installation

```
pip install ipfabric
```

To run examples please specify the extras option during install:
```
pip install ipfabric -E examples
```

## Introduction

Please take a look at [API Programmability - Part 1: The Basics](https://ipfabric.io/blog/api-programmability-part-1/)
for instructions on creating an API token.

Most of the methods and features can be located in [Examples](examples) to show how to use this package. 
Another great introduction to this package can be found at [API Programmability - Part 2: Python](https://ipfabric.io/blog/api-programmability-python/)

## Diagrams

Diagramming in IP Fabric version v4.3 and above has been moved to it's own package.  The diagramming included in
this package will work for version >= v4.0 and < v4.3.

```
pip install ipfabric-diagrams
```

## Authentication
### Basic
Please take a look at [basic.py](examples/basic.py) for basic authentication examples

### Environment 
The easiest way to use this package is with a `.env` file.  You can copy the sample and edit it with your environment variables. 

```commandline
cp sample.env .env
```

This contains the following variables which can also be set as environment variables instead of a .env file.
```
IPF_URL="https://demo3.ipfabric.io"
IPF_TOKEN=TOKEN
IPF_VERIFY=true
```

**`IPF_DEV` is an internal variable only, do not set to True.**

## Development

IPFabric uses poetry for the python packaging module. Install poetry globally:

```
pip install poetry
```

To install a virtual environment run the following command in the root of this directory.

```
poetry install
```

To test and build:

```
poetry run pytest
poetry build
```

GitHub Actions will publish and release. Make sure to tag your commits:

* ci: Changes to our CI configuration files and scripts
* docs: No changes just documentation
* test: Added test cases
* perf: A code change that improves performance
* refactor: A code change that neither fixes a bug nor adds a feature
* style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning). 
* feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning). 
* BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking
API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
