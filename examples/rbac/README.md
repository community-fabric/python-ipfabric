# RBAC Configuration Script
This example repo provides some default policies that the Solution Architecture team at IP Fabric have created to create read/write policies and roles for a number of common tasks.

## Installation

```
git clone git@github.com:community-fabric/python-ipfabric.git
cd python-ipfabric/examples/rbac
pip install -r requirements.txt
```

## Usage
To use this example there are a number of things to do.

- Configure environment variables
    - `export IPF_URL=https://<replace with your ipf url>`
    - `export IPF_TOKEN=<replace with your ipf api token>`

```bash
> python -m main --help
usage: IP Fabric RBAC Script [-h] [--roles ROLES] [--policies POLICIES] [--delete-all] [--verify] [--version VERSION] [--verbose]

Configures IP Fabric RBAC Policies from YAML files.

options:
  -h, --help           show this help message and exit
  --roles ROLES        Path to roles YAML file.
  --policies POLICIES  Path to policies YAML file.
  --delete-all         Delete all RBAC none default roles and policies.
  --verify             This will disable SSL certificate verification.
  --version VERSION    Specify API Version.
  --verbose            Enable stdout console logging.
```

### Install Policies and Roles

```bash
python -m main
or
python main.py
```

### Delete Policies and Roles

```bash
python -m main --delete-all
or
python main.py --delete-all
```
