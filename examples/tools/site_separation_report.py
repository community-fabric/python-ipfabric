import pandas as pd

from ipfabric import IPFClient
from ipfabric.tools import map_devices_to_rules

if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    devices = map_devices_to_rules(ipf)

    df = pd.DataFrame(devices)
    df.to_csv('SiteSeparation.csv', index=False)

    print(devices[0])
    