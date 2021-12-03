"""
api_tokens.py
"""
from pprint import pprint

from ipfabric import IPFClient
from ipfabric.settings import APIToken

if __name__ == '__main__':
    ipf = IPFClient('https://demo3.ipfabric.io/')  # Token must have Setting Permissions
    ipf_tokens = APIToken(client=ipf)

    pprint(ipf_tokens.tokens)
    """
    [{'description': 'Justin',
    'expires': None,
    'id': '1158890326',
    'isExpired': False,
    'lastUsed': 1638558821109,
    'maxScope': ['read', 'write', 'settings'],
    'scope': ['read', 'write', 'settings'],
    'usage': 9603,
    'userId': '1108612054',
    'username': 'justin'},
    ...]
    """
    print()

    token = ipf_tokens.add_token('Token Description', ['read'], expires='12/30/2021')  # Expires is optional
    # Scope must be in ['read', 'write', 'settings', 'team']
    # Can also specify token='TOKENNAME', must be 8 or more characters
    print(token)
    """
    {'token': '729b1714e0e732af95e8e5e5c9fb39db', 'response': {'description': 'Token Description', 
    'expires': 1640840400000, 'lastUsed': None, 'scope': ['read'], 'usage': 0, 'id': '1166335283', 
    'userId': '1108612054', 'username': 'justin', 'isExpired': False}}
    """
    print()

    delete = ipf_tokens.delete_token(token['response']['id'])
    print(len(delete))
    """
    6
    """
