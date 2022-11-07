"""
attributes.py
"""
from pprint import pprint

import pandas as pd

from ipfabric import IPFClient
from ipfabric.settings import Attributes

if __name__ == '__main__':
    ipf = IPFClient()  # Token must have Setting Permissions
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    ipf_attr = Attributes(client=ipf)

    """
    Export Device Inventory table to CSV.
    Required columns with headers (API column names): Site (siteName), Unique serial number (sn)
    Edit Site column with corrected Site Name (case sensitive).
    """
    df = pd.read_csv(r'sites.csv')

    site_attributes = [{'value': row['Site'], 'sn': row['Unique serial number']} for index, row in df.iterrows()]

    sites = ipf_attr.set_sites_by_sn(site_attributes)

    pprint(sites)
    """
    [{'id': '9786859055',
      'name': 'siteName',
      'sn': 'a23ffc0',
      'value': '35HEADOFFICE'},
        ...]
    """
    attributes = [
        dict(serial_number='a23ffc0', name='FLOOR', value='1'),
        dict(serial_number='a23ffbe', name='FLOOR', value='2')
    ]
    resp = ipf_attr.set_attribute_by_sn(**attributes[0])  # Set a single attribute, will fail if already set
    resp = ipf_attr.set_attributes_by_sn(attributes)  # Set a list of attributes, will update if already set

    """
    Attribute names must match this regex: ^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]+$
    """

    resp = ipf_attr.delete_attribute(*sites)  # Delete a list of attributes
    resp = ipf_attr.delete_attribute_by_id('9786859055')  # Delete attribute by ID
    resp = ipf_attr.delete_attribute_by_sn('a23ffc0')  # Delete attribute by sn
