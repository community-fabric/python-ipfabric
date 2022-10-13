# Installing Python IP Fabric

## Minimum Requirements

* Python 3.7+
* Access to an Instance of IP Fabric
* API Token or Username and password to IP Fabric

## Poetry (Recommended)

Poetry is a python package manager that makes spinning up a Virtual Enviroment ready to run your code quick and easy.

Make sure we have Poetry installed in our python environment
```shell
pip install poetry 
```
Since Poetry manages all our required packages, we only have to run one command to install all the dependencies required for Python IPFabric
```shell
poetry install  
```

want to install all the dependencies required to run our example scripts? 
```shell
poetry install -E examples
```

## pip

```shell
pip install ipfabric
```

to run scripts in the example directory
```shell
pip install ipfabric[examples]
```

