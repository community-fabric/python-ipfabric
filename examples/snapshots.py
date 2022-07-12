"""
snapshots.py
"""
from pprint import pprint
from time import sleep

from ipfabric import IPFClient

if __name__ == '__main__':
    """
    Example with no loaded snapshots
    Python 3.9.9 (tags/v3.9.9:ccb0e6a, Nov 15 2021, 18:08:50) [MSC v.1929 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from ipfabric import IPFClient
    >>> ipf = IPFClient()
    No Snapshots are currently loaded.  Please load a snapshot before querying any data.
    >>> ipf.unloaded_snapshots.keys()
    dict_keys(['ea0da479-6222-4cf6-a0ae-78a610669477', '5895196e-8144-4c97-b081-b76e725bfd2c', '30515074-1741-461d-9241-f4831fe46d51'])
    >>> ipf.snapshots['ea0da479-6222-4cf6-a0ae-78a610669477'].load(ipf)
    True
    >>> ipf.update()
    >>> ipf.loaded_snapshots.keys()
    dict_keys(['ea0da479-6222-4cf6-a0ae-78a610669477', '$last'])
    >>> ipf.loaded_snapshots['$last'].unload(ipf)
    True
    """

    ipf = IPFClient(snapshot_id="$prev")
    # ipf = IPFClient('https://demo3.ipfabric.io/', snapshot_id="$lastLocked", token='token', verify=False, timeout=15)

    print(f"IP Fabric version: {ipf.os_version}")
    """
    IP Fabric version: 4.0.2
    """

    print(f"Class snapshot id is set to {ipf.snapshot_id}")
    print(f"Latest snapshot id is \t\t{ipf.snapshots['$last'].snapshot_id}")
    """
    Class snapshot id is set to d3bd033e-1ba6-4b27-86f5-18824a1a495e
    Latest snapshot id is	    c8684ea9-dfd8-400d-a4b8-ba1c4bc7c185
    """

    print("Print a snapshot object: ")
    pprint(ipf.snapshots[ipf.snapshot_id])
    """
    Print a snapshot object: 
    {
     'count': 640,
     'end': datetime.datetime(2021, 10, 21, 12, 37, 3, 513000),
     'snapshot_id': 'd3bd033e-1ba6-4b27-86f5-18824a1a495e',
     'state': 'loaded',
     'locked': True,
     'name': 'Baseline 10-21',
     'start': datetime.datetime(2021, 10, 21, 11, 59, 54, 941000)
     'loaded': True # Class Property
     }
    """

    # Unload and load snapshots
    ipf.snapshots['$last'].unload(ipf)

    sleep(240)
    ipf.update()
    ipf.snapshots['c8684ea9-dfd8-400d-a4b8-ba1c4bc7c185'].load(ipf)
