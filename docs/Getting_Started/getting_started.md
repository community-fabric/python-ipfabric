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
# Using the SDK

## Setting up an API Token
Please follow directions found [here](https://docs.ipfabric.io/5.0/IP_Fabric_Settings/api_tokens/)

## Environment Variables
Please add the following environment variables to your .env file. 

| Variable Name | Python Parameter | Default |        Description |
|---------------|:----------------:|--------:|-------------------:|
| IPF_URL       |     base_url     |    None | IP Fabric instance |
| IPF_TOKEN     |      token       |    None |          API token |
| IPF_VERIFY    |      verify      |    True |        Enforce SSL |

## Initializing 
Once you set up your environment variables: 
<script id="asciicast-Wsz5iaI3zRSSyZkd0trmpXDSq" src="https://asciinema.org/a/Wsz5iaI3zRSSyZkd0trmpXDSq.js" async data-autoplay="true" data-speed="2" data-loop="1"></script>


## Inventory
to quickly get an inventory of devices or interfaces: 
```python
>>> ipf.inventory.devices.all()
>>> ipf.inventory.interfaces.all()
```
## Technology

For each Technology Table in IP Fabric, we have a way to quickly gather the data

```python
>>> ipf.technology.
ipf.technology.addressing            ipf.technology.managed_networks 
ipf.technology.client                ipf.technology.port_channels
ipf.technology.cloud                 ipf.technology.platforms
ipf.technology.dhcp                  ipf.technology.qos
ipf.technology.routing               ipf.technology.oam
ipf.technology.fhrp                  ipf.technology.security
ipf.technology.interfaces            ipf.technology.sdn
ipf.technology.ip_telephony          ipf.technology.sdwan
ipf.technology.load_balancing        ipf.technology.stp
ipf.technology.mpls                  ipf.technology.vlans
ipf.technology.multicast             ipf.technology.wireless
ipf.technology.neighbors             ipf.technology.management
```

Each one of these technologies relates to data IP Fabric has gathered about your network devices.
For example to view ntp configurations:

```python
ipf.technology.management.ntp_summary.all()
```