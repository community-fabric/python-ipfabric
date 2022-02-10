"""
intent_reports.py
"""
from tabulate import tabulate

from ipfabric import IPFClient

# Requires openpyxl also for Excel reports


if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    ipf.intent.load_intent()  # Load Intent Checks
    # ipf.intent.load_intent('$prev') Load a different snapshot into the class overriding the client.

    compare = ipf.intent.compare_snapshot("$lastLocked", reverse=True)
    print(tabulate(compare, headers="keys"))
    """
    Current: The snapshot loaded into the intent class:
        ipf.intent.load_intent('$last')
    Other: The snapshot in the comparison:
        ipf.intent.compare_snapshot('$prev', reverse=True)
    Reverse (Default: False): Will flip current and other.  Use when class is newest date and compare is an older date.
    
    name                                                  id  check      loaded_snapshot    compare_snapshot    diff
    --------------------------------------------  ----------  -------  -----------------  ------------------  ------
    CDP/LLDP unidirectional                        320633253  total                   25                  18      -7
    CDP/LLDP unidirectional                        320633253  blue                    25                  18      -7
    BGP Session Age                                322316677  total                  367                 358      -9
    BGP Session Age                                322316677  green                  309                 305      -4
    BGP Session Age                                322316677  blue                    22                  19      -3
    BGP Session Age                                322316677  amber                    3                   0      -3
    BGP Session Age                                322316677  red                     33                  33       0
    """



