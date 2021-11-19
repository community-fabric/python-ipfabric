"""
graphs.py
"""
from ipfabric import IPFClient
from pprint import pprint


if __name__ == '__main__':
    ipf = IPFClient('https://demo3.ipfabric.io/')
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    data = ipf.graphs.host_to_gw('10.47.117.112')
    pprint(data)
    """
    {'graphResult': {'boxLabels': {'L47': 'L47'},
                     'graphData': {'edges': {'host-10.47.117.112--vDevice/1149345216@Et0/0--#0': ...},
                                   'nodes': {'host-10.47.117.112': {'boxId': 'L47',
                                                                    'children': [],
                                                                    'graphType': 'pathLookup',
                                                                    'id': 'host-10.47.117.112',
                                                                    'label': 'host: '
                                                                             '10.47.117.112',
                                                                    ...,
                                                                    'type': 'host'},
                                             'vDevice/1148575691': {'boxId': 'L47',
                                                                    ...
                                                                    'type': 'switch'},
                                             ...},
                     'settings': {...},
     'pathlookup': {'check': {'exists': False},
                    'decisions': {...},
                    'eventsSummary': {...},
                    'passingTraffic': 'all'}}
    """

    ipf.graphs.style = 'svg'  # Default is json, but can be svg or png, svg/png will return bytes data
    params = {
        "src_ip": "10.47.117.112",  # Can be IP or /24 or smaller subnet
        "dst_ip": "10.66.126.0/24",  # Can be IP or /24 or smaller subnet
        "proto": "tcp",  # Default must be tcp, udp, or icmp
        "src_port": 10000,  # Default
        "dst_port": 80,  # Default
        "sec_drop": True,  # Default
        "grouping": "siteName",  # Default
        "flags": None,  # Default, if tcp and defined must be a list with values in
                        # ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        "snapshot_id": None  # Default, used to override class snapshot
    }
    data = ipf.graphs.unicast(**params)
    with open('test.svg', 'wb') as f:
        f.write(data)

    ipf.graphs.style = 'png'
    params = {
        "src_ip": "10.33.230.2",  # Must be IP
        "grp_ip": "233.1.1.1",  # Must be IP
        "rec_ip": "10.33.244.200",  # Optional, must be a single IP if used
        "proto": "udp",  # Default is tcp
        "src_port": 10000,  # Default
        "grp_port": 80,  # Default
        "sec_drop": True,  # Default
        "grouping": "siteName",  # Default
        "flags": None,  # Default
        "snapshot_id": None  # Default, used to override class snapshot
    }
    data = ipf.graphs.multicast(**params)
    with open('test.png', 'wb') as f:
        f.write(data)
