"""
security.py
"""
from pprint import pprint

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient('https://demo3.ipfabric.io/')
    policies = ipf.security.search_acl_policies('L72AC26')
    pprint(policies)
    """
    [{'defaultAction': 'deny',
    'hostname': 'L72AC26',
    'id': '1153623227',
    'name': 'CISCO-CWA-URL-REDIRECT-ACL',
    'siteKey': '885963582',
    'siteName': 'L72',
    'sn': 'a48ff83'}]
    """
    print()

    policy = ipf.security.get_policy(policies[0])  # Takes a policy dictionary or a string with the sn of the policy
    pprint(policy)
    """
    Policy(hostname='L72AC26', security={'machineAcl': {'entryChainName': ...})
    """
    print()

    policies = ipf.security.search_zone_policies()  # No hostname will return all policies
    pprint(policies[0])
    """
    {'defaultAction': 'deny',
    'hostname': 'L71FW14',
    'id': '1153757631',
    'name': 'main',
    'siteKey': '885963247',
    'siteName': 'L71',
    'sn': 'FGVMEV9VFR6KQI1A'}
    """