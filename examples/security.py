"""
security.py
"""
from pprint import pprint

from ipfabric import IPFClient

if __name__ == '__main__':
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    policies = ipf.security.search_acl_policies('L39EXR11')
    pprint(policies)
    """
    [{'defaultAction': 'deny',
    'hostname': 'L39EXR11',
    'id': '1154551838',
    'name': 'EFILTER',
    'siteKey': '885963413',
    'siteName': 'L39',
    ...]
    """
    print()

    policy = ipf.security.get_policy(policies[0])  # Takes a policy dictionary or a string with the sn of the device
    pprint(policy.__dict__)  # This returns all Policies on the device, not just the one in question
    """
    {'hostname': 'L39EXR11',
    'machine_acl': {'BC': <ipfabric.security.RuleChain object at 0x00000255E4732610>,
                 'BLOCK-TELNET': <ipfabric.security.RuleChain object at 0x00000255E4732730>,
                 'EF': <ipfabric.security.RuleChain object at 0x00000255E4732640>,
                 'EFILTER': <ipfabric.security.RuleChain object at 0x00000255E46DF100>,
                 'OAM': <ipfabric.security.RuleChain object at 0x00000255E4732850>,
                 '_entryRuleChain': <ipfabric.security.RuleChain object at 0x00000255E47326D0>,
                 'inputChain': <ipfabric.security.RuleChain object at 0x00000255E4732820>,
                 'outputChain': <ipfabric.security.RuleChain object at 0x00000255E4732880>},
    'machine_zones': None,
    'named_tests': None,
    'named_values': None}
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
    print()

    policies = ipf.security.search_zone_policies('L66JFW9')  # No hostname will return all policies
    policy = ipf.security.get_policy(policies[0])  # Takes a policy dictionary or a string with the sn of the device
    pprint(policy.__dict__)
    """
    {'hostname': 'L66JFW9',
     'machine_acl': {'_entryRuleChain': <ipfabric.security.RuleChain object at 0x000002275CE63580>,
                     'inputChain': <ipfabric.security.RuleChain object at 0x000002275CE635B0>,
                     'outputChain': <ipfabric.security.RuleChain object at 0x000002275CE7CA00>},
     'machine_zones': {'HOST120@wan': <ipfabric.security.RuleChain object at 0x000002275CE7CA30>,
                       'HOST121@wan': <ipfabric.security.RuleChain object at 0x000002275CE7CEE0>,
                       'HOST122@wan': <ipfabric.security.RuleChain object at 0x000002275CE7CEB0>,
                       .},
     'zones': {'ge-0/0/2.120': ['HOST120'],
               'ge-0/0/2.121': ['HOST121'],
               ...},
     'named_tests': {'zoneFw_application_DNS': {'category': 'application',
                                                'group': 'or',
                                                'items': [{'category': 'application',
                                                           'group': 'and',
                                                           'items': [{'left': {'field': 'protocol',
                                                                               'header': 'ip'},
                                                                      'operator': 'num==',
                                                                      'right': {'original': 'tcp',
                                                                                'type': 'number',
                                                                                'value': 6}},
                                                                     {'left': {'field': 'dst',
                                                                               'header': 'tcp'},
                                                                      'operator': 'numset-matches',
                                                                      'right': {'original': '53',
                                                                                'type': 'numberSet',
                                                                                'value': [{'max': 53,
                                                                                           'min': 53}]}}],
                                                           'name': 'DNS'},
                                                          {'category': 'application',
                                                           'group': 'and',
                                                           'items': [{'left': {'field': 'protocol',
                                                                               'header': 'ip'},
                                                                      'operator': 'num==',
                                                                      'right': {'original': 'udp',
                                                                                'type': 'number',
                                                                                'value': 17}},
                                                                     {'left': {'field': 'dst',
                                                                               'header': 'udp'},
                                                                      'operator': 'numset-matches',
                                                                      'right': {'original': '53',
                                                                                'type': 'numberSet',
                                                                                'value': [{'max': 53,
                                                                                           'min': 53}]}}],
                                                           'name': 'DNS'}],
                                                'name': 'DNS'},
                     },
     'named_values': {'numberSet': {'zoneFw_ADD-BOOK01_NET4_BOGON01': {'category': 'Address',
                                                                       'name': 'NET4_BOGON01 '
                                                                               '(ADD-BOOK01)',
                                                                       'original': '192.168.0.0/16',
                                                                       'type': 'numberSet',
                                                                       'value': [{'max': 3232301055,
                                                                                  'min': 3232235520}]},
                                    }
                    }
    }
    """