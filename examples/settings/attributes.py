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

    resp = ipf_attr.set_sites_by_sn(site_attributes)

    pprint(resp)
    """
    [{'id': '9786859055',
      'name': 'siteName',
      'sn': 'a23ffc0',
      'value': '35HEADOFFICE'},
        ...]
    """