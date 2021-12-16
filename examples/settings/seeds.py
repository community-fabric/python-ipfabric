"""
seeds.py
"""
from ipfabric import IPFClient
from ipfabric.settings import Seeds


if __name__ == '__main__':
    ipf = IPFClient()  # Token must have Setting Permissions
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    ipf_seeds = Seeds(client=ipf)

    print(ipf_seeds.seeds)
    """
    ['10.64.128.3', '10.64.128.1', '10.66.255.105', '10.67.255.108', '10.67.255.107']
    """
    print()

    add = ipf_seeds.add_seeds('127.0.0.1')  # Can be a single IP or list
    print(add)
    """
    ['10.64.128.3', '10.64.128.1', '10.66.255.105', '127.0.0.1', '10.67.255.107', '10.67.255.108']
    """
    print()

    delete = ipf_seeds.delete_seeds('127.0.0.1')  # Can be a single IP or list
    print(delete)
    """
    ['10.66.255.105', '10.64.128.3', '10.67.255.108', '10.64.128.1', '10.67.255.107']
    """
    print()

    update = ipf_seeds.set_seeds(["10.64.128.3", "10.64.128.1", "10.66.255.105", "10.67.255.108", "10.67.255.107"])
    # Will replace the entire configuration with this new list
    print(update)
    """
    ['10.64.128.3', '10.64.128.1', '10.66.255.105', '10.67.255.108', '10.67.255.107']
    """
    print()
