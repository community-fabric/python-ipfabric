# IPFabric

IPFabric is a Python module for connecting to and communicating against an IP Fabric instance.

## About

Founded in 2015, [IP Fabric](https://ipfabric.io/) develops network infrastructure visibility and analytics
solution to help enterprise network and security teams with network assurance and automation across multi-domain
heterogeneous environments. From in-depth discovery, through graph visualization, to packet walks and complete network
history, IP Fabric enables to confidently replace manual tasks necessary to handle growing network complexity driven by
relentless digital transformation.

## Installation

```
pip install ipfabric
```

## Introduction

## Development

IPFabric uses poetry for the python packaging module. Install poetry globally:

```
pip install poetry
```

To install a virtual environment run the following command in the root of this directory.

```
poetry install
```

To test, build, and publish:

```
poetry run pytest
poetry build
poetry publish
```
