"""
intent.py
"""
from pprint import pprint

from ipfabric import IPFClient

if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    ipf.intent.load_intent()  # Load Intent Checks
    # ipf.intent.load_intent('$prev') Load a different snapshot into the class overriding the client.

    intents = ipf.intent.get_intent_checks("$lastLocked")  # Returns checks for a snapshot, does not load in the class

    pprint(ipf.intent.intent_checks[0].__dict__)
    """
    {'api_endpoint': '/v1/tables/neighbors/unidirectional',
     'checks': Checks(green=None, blue=None, amber=None, red=None),
     'column': 'localHost',
     'custom': False,
     'default_color': 10,
     'descriptions': Description(general='Detects unidirectional Cisco Discovery Protocol (CDP) or 
        Link-Layer Discovery Protocol (LLDP) sessions.\n', 
        checks=Checks(green='', blue='Unidirectional CDP or LLDP sessions.', amber='', red='')),
     'groups': [Group(custom=True, name='Neighborship compliance', group_id='320668119', children=[])],
     'intent_id': '320633253',
     'name': 'CDP/LLDP unidirectional',
     'result': Result(count=21, checks=Checks(green=None, blue='21', amber=None, red=None)),
     'status': 1,
     'web_endpoint': '/technology/cdp-lldp/unidirectional-neighbors'}
    """
    print()

    print(f"Number of custom checks {len(ipf.intent.custom)}")
    """Number of custom checks 25"""
    print()

    print(f"Number of builtin checks {len(ipf.intent.builtin)}")
    """Number of builtin checks 132"""
    print()

    print(f"{ipf.intent.intent_by_name['OSPF Neighbor State'].name} belongs to the following groups.")
    for g in ipf.intent.intent_by_name["OSPF Neighbor State"].groups:
        print(g.name)
    """"
    OSPF Neighbor State belongs to the following groups.
    Neighborship compliance
    """
    print()

    end_of_support = ipf.intent.get_all_results(ipf.intent.intent_by_name["End of Support"])
    print(end_of_support.result_data)
    """
    green=[{'id': '1629809283640666', 'dscr': 'SG300-10PP 10-port Gigabit PoE+ Managed Switch', 
            'endMaintenance': {'data': None, 'severity': -1}, 'endSale': {'data': 1525910400000, ml',...] 
    blue=None 
    amber=None
    red=[{'id': '1632632890662679', 'dscr': '4400 Series WLAN Controller for up to 25 Lightweight APs', 
    'endMaintenance': {'data': 1339495200000, 'severity': 20}, 'endSale': {'data': 1307959200000, ...]
    """

    print(f"{ipf.intent.builtin[1].name} has  a total of {ipf.intent.builtin[1].result.count} matches.")
    """"
    BGP Session Age has  a total of 344 matches.
    """
    print()

    results = ipf.intent.get_results(ipf.intent.builtin[2], "amber")
    # Takes in an intent rule and the color you want to view
    # Colors are green (0), blue (10), amber (20), red (30)
    print(f"{ipf.intent.builtin[2].name} has {len(results)} that are amber.")
    print(f"Amber means {ipf.intent.builtin[2].descriptions.checks.amber}.")
    print(results[0])
    """
    IPSec Tunnel Encryption has 3 that are amber.
    Amber means IPSec tunnels with insecure/weak encryption algorithm.
    
    {'id': '1153299800', 'authentication': {'data': 'md5', 'severity': 20}, 'autoUp': None, 'dhGroup': None, 
    'encapsulation': 'tunnel', 'encryption': {'data': '3des', 'severity': 20}, 
    'hostname': 'L71FW5_hasAVeryLongHostname', 'ikeGateway': 'ipsec_L64_mtik', 'intDscr': None, 'intName': 'port4', 
    'keepAlive': None, 'keyLifeBytes': None, 'keyLifeSeconds': 600, 'localGwAddress': '10.71.109.105', 
    'neighbors': [], 'profileName': 'ipsec_L64_mtik_loop', 'protocol': 'esp', 'remoteGwAddress': '10.64.104.103', 
    'routeBased': True, 'selectorLocalAddress': '10.71.200.1/32', 'selectorLocalPort': None, 'selectorProtocol': None, 
    'selectorRemoteAddress': '10.64.200.1/32', 'selectorRemotePort': None, 'siteKey': '885963247', 'siteName': 'L71', 
    'sn': 'FOSVM1QWZRUM4EB7', 'status': {'data': 'up', 'severity': 0}, 'tunnelIntName': 'ipsec_L64_mtik'}
    """
    print()
