"""
attributes.py
"""

from ipfabric import IPFClient
from ipfabric.settings import Attributes

if __name__ == '__main__':
    ipf = IPFClient()  # Token must have Setting Permissions
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    ipf_attr = Attributes(client=ipf, snapshot_id='$last')

    """
    Local (Snapshot Specific) Attributes has all the same methods as seen in attributes.py examples.
    
    THERE IS NO POST METHOD FOR LOCAL ATTRIBUTES.  This means that adding an attribute will overwrite current value 
    instead of erroring if already present.
    
    There is one method that applies to local but not global: 
    """

    resp = ipf_attr.update_local_attr_from_global()
    """
    This will delete all Local Attributes and apply the Global Settings.
    It will return True if successful.
    """
