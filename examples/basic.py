"""
basic.py
"""

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient(unloaded=False)
    """
    Default: unloaded=False
    Set to True to get metadata from all unloaded snapshots.
    Collecting unloaded snapshot metadata could increase memory requirements significantly depending on how many
    unloaded snapshots are on your system.
    """
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    print(ipf.get_count('tables/management/ntp/summary'))
    # or:
    print(ipf.technology.management.ntp_summary.count())

    ntp = ipf.fetch_all('tables/management/ntp/summary')
    # or:
    ntp = ipf.technology.management.ntp_summary.all()
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
    filters = {
        "source": [
            "like",
            "10.0.10.10"
        ]
    }
    ntp_sources = ipf.fetch_all('tables/management/ntp/sources', filters=filters)
    # or:
    ntp_sources = ipf.technology.management.ntp_sources.all(filters=filters)
    print(ntp_sources[0])
    """
    {'id': '1448791314', 'delay': 3.922, 'flags': ['sys.peer', 'configured'], 'hostname': 'L38AC14', 'jitter': 1.091, 
    'offset': 0.483, 'poll': 1024, 'reach': 377, 'reachable': 'yes', 'reference': '5.1.56.123', 'siteKey': '885963537', 
    'siteName': 'L38', 'sn': 'a26ff9f', 'source': '10.0.10.10', 'stratum': 3, 'when': 732}
    """
