"""
attribute_filter.py
"""

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    print(ipf.inventory.devices.count())
    # 512

    ipf.attribute_filters = {"FLOOR": ["12"]}
    """
    Setting Global Attribute Filter for all tables/diagrams until explicitly unset to None.
    This may cause errors on some tables like in Settings.
    Adding an Attribute Filter to any function will overwrite the Global Filter.
    Filter: {'FLOOR': ['12']}
    """

    print(ipf.inventory.devices.count())
    # 1