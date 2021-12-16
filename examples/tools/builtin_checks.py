from tabulate import tabulate

from ipfabric import IPFClient
from ipfabric.tools import SinglePointsFailure, NonRedundantLinks

if __name__ == "__main__":
    # USE SPARINGLY THIS WILL CREATE A GRAPH OF ALL YOUR SITES.
    # NOT TESTED ON AN IP FABRIC INSTANCE WITH MORE THAN 1,000 DEVICES
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    nrl = NonRedundantLinks(ipf)
    links = nrl.list()

    print(tabulate(links, headers="keys"))
    """
    source                source_int     target             target_int
    --------------------  -------------  -----------------  ------------
    L71R3                 Et1/1          L71FW10-HA2/root   vl201
    L67FW31               ge-0/0/3.0     L67P13             ge-0/0/4.0
    L71-CP1/0             wrp0           L71EXR2            Et0/3
    L71-CP1/BadCompany    eth1           L71R4              Et1/1
    """
    print()

    spf = SinglePointsFailure(ipf)
    nodes = spf.list()
    print(tabulate(nodes, headers="keys"))
    """
    device                type
    --------------------  ------------------
    HWLAB                 router
    HWLAB-sw3_5650TD      switch
    HWLAB-FW-RBSH1        waas
    HWLAB-FW-C5510/admin  fw
    HWLAB-WLC-A620        wlc
    HWLAB-FPR-1010        fw
    HWLAB-WLC-C4400       wlc
    """
