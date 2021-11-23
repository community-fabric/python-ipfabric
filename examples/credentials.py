"""
credentials.py
"""
from ipfabric import IPFClient
from ipfabric.settings import Authentication
from pprint import pprint


if __name__ == '__main__':
    ipf = IPFClient('https://demo3.ipfabric.io/')  # Token must have Setting Permissions
    ipf_auth = Authentication(client=ipf)

    credentials = ipf_auth.credentials
    pprint(credentials[1])  # Priority starts at 1
    """
    Credential(network=['0.0.0.0/0'], excluded=[], expiration=Expiration(enabled=False, value=None), 
    credential_id='918d1a0f-98b1-4895-ba51-340f7f2cf6cd', encrypt_password='829ec229e38314', priority=1, 
    username='admin15', config_mgmt=True, notes=None)
    """
    print()

    enables = ipf_auth.enables  # Enable secrets, API is named Privilege
    pprint(enables[1])  # Priority starts at 1
    """
    Privilege(network=['0.0.0.0/0'], excluded=[], expiration=Expiration(enabled=False, value=None), 
    privilege_id='0a5b528d-4fd1-4e62-91e7-e565affa058f', encrypt_password='829ec229e38314', 
    priority=1, username='admin15', notes=None)
    """
    print()

    cred = ipf_auth.create_credential('test', 'password', notes='Test for Blog', config_mgmt=True)
    pprint(cred)
    """
    Credential(network=['0.0.0.0/0'], excluded=[], expiration=Expiration(enabled=False, value=None),
    credential_id='f761ff06-7d8d-4e57-b6d2-4a00d59b623e', encrypt_password='939bdc33fadd5316', priority=None,
    username='979fdc34', config_mgmt=True, notes='Test for Blog')
    """
    print()

    enable = ipf_auth.create_enable('test', 'password', notes='Test for Blog',
                                    networks=['10.0.0.0/24'], excluded=['10.0.0.0/30'], expiration='12-30-2021')
    pprint(enable)
    """
    Privilege(network=['10.0.0.0/24'], excluded=['10.0.0.0/30'], 
    expiration=Expiration(enabled=True, value=datetime.datetime(2021, 12, 30, 0, 0)), 
    privilege_id='180116e4-11c5-454b-8a37-64f7406f5a6b', encrypt_password='939bdc33fadd5316', 
    priority=None, username='979fdc34', notes='Test for Blog')
    """

