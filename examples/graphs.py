"""
graphs.py
"""
from pprint import pprint

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    site = ipf.graphs.site('MPLS')
    print(site)
    """
    {'graphResult': {'graphData': {'edges': {'1155361666': {'direction': 'bidirected', 'shift': -0.5, 
    'source': 'a15ff01', 'target': 'a15ff0b', 'circle': False, 'edgeSettingsId': 'c406f1d0-3ec5-4469-8449-a3265e55fe38',
     'children': ['1155361666'], 'id': '1155361666', 'style': {'line': {'pattern': 'solid', 'color': 7321967, 
     'thickness': 1}}, 'labels': {'center': [{'type': 'protocol', 'visible': True, 'text': 'L1'}], 'source': 
     [{'type': 'intName', 'visible': False, 'text': 'Et0/1'}], 'target': 
     [{'type': 'intName', 'visible': False, 'text': 'Et0/0'}]}, 'protocol': 'xdp', 'positions': 
     {'arrowHeads': {'target': [{'x': 379.076321934...
    """

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
