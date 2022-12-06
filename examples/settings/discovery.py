from ipfabric import IPFClient
from ipfabric.settings.discovery import Discovery

if __name__ == '__main__':
    ipf = IPFClient()
    ipf_discovery = Discovery(ipf)
    subnets = ['10.1.2.0/24', '10.1.3.0/24']
    ipf_discovery.update_discovery_networks(subnets)
    print(ipf_discovery.networks)
    """
    exclude=['10.1.2.0/24', '10.1.3.0/24'] include=['0.0.0.0/0']
    """
    subnets = ['10.1.1.0/24']
    ipf_discovery.update_discovery_networks(subnets, include=True)
    print(ipf_discovery.networks)
    """
    exclude=['10.1.2.0/24', '10.1.3.0/24'] include=['10.1.1.0/24']
    """

