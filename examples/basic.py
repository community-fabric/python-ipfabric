"""
basic.py
"""

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    print(ipf.get_count('tables/management/ntp/summary'))

    ntp = ipf.fetch_all('tables/management/ntp/summary')
    print(len(ntp))
    print()
    print(ntp[0])
    """
    435
    435

    {'id': '1448808110', 'confSources': 1, 'hostname': 'L36AC43', 'reachableSources': 1, 'siteKey': '885963685', 
    'siteName': 'L36', 'sn': 'a24ff82', 'sources': [{'source': '10.0.10.10', 'sync': True}]}
    """

    print()
    ntp_sources = ipf.fetch_all('tables/management/ntp/sources', filters={
        "source": [
            "like",
            "10.0.10.10"
        ]
    })
    print(ntp_sources[0])
    """
    {'id': '1448791314', 'delay': 3.922, 'flags': ['sys.peer', 'configured'], 'hostname': 'L38AC14', 'jitter': 1.091, 
    'offset': 0.483, 'poll': 1024, 'reach': 377, 'reachable': 'yes', 'reference': '5.1.56.123', 'siteKey': '885963537', 
    'siteName': 'L38', 'sn': 'a26ff9f', 'source': '10.0.10.10', 'stratum': 3, 'when': 732}
    """
