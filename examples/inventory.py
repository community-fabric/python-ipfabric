"""
inventory.py
"""
from pprint import pprint

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    print([x for x in dir(ipf.inventory) if not x.startswith('_')])
    """
    ['devices', 'families', 'interfaces', 'models', 'part_numbers', 'platforms', 'sites', 'vendors']
    """
    print()

    sites = ipf.inventory.sites.all()
    print(f"Number of sites: {len(sites)}")
    print("First site:")
    pprint(sites[0])
    """
    Number of sites: 25
    First site:
    {'devicesCount': 22,
     'id': '1111118694',
     'siteKey': '1111118694',
     'siteName': 'HWLAB',
     'siteUid': 'HWL',
     ...}
    """
    print()

    devices = ipf.inventory.devices.all(filters={
        "siteName": [
            "like",
            "L71"
        ]
    })
    """
    Also acceptable if filter is string
    devices = ipf.inventory.devices.all(filters='{"siteName": ["like","L71"]}')
    """
    print(f"Number of devices in site L71: {len(sites)}")
    print("First Device:")
    pprint(devices[0])
    """
    Number of devices in site L71: 25
    First Device:
    {'devType': 'fw',
     'family': 'fortigate',
     'hostname': 'L71FW13-HA2/root',
     'id': '1137600732',
     ...}
     """
    print()

    vendors = ipf.inventory.vendors.all(columns=["vendor"])

    print(f"Number of vendors: {len(vendors)}")
    [print(vendor["vendor"]) for vendor in vendors]
    """
    Number of vendors: 14
    arista
    aws
    checkpoint
    cisco
    ...
    """
