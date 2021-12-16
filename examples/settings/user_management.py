"""
user_management.py
"""
from ipfabric import IPFClient
from ipfabric.settings import UserMgmt


if __name__ == '__main__':
    ipf = IPFClient()  # Token must have User Management Permissions
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    usermgmt = UserMgmt(client=ipf)

    print(usermgmt.users[0])
    """
    username='justin' scope=['read', 'write', 'settings'] email='justin.jeffrey@ipfabric.io' user_id='1108612054' 
    local=True sso_provider=None domains='' custom_scope=True ldap_id=None
    """
    print()

    user = usermgmt.add_user(username='Test', email='test@ipfabric.io', password='8characters',
                             scope=['read', 'write', 'settings', 'team'])
    print(user)
    """
    username='Test' scope=['read', 'write', 'settings', 'team'] email='test@ipfabric.io' user_id='1168572704' 
    local=None sso_provider=None domains=None custom_scope=True ldap_id=None
    """
    print()

    print(usermgmt.get_user_by_id(user_id=user.user_id))
    """
    username='Test' scope=['read', 'write', 'settings', 'team'] email='test@ipfabric.io' user_id='1168572704' 
    local=None sso_provider=None domains=None custom_scope=True ldap_id=None
    """
    print()

    print(usermgmt.get_users(username=user.username))
    """
    [User(username='Test', scope=['read', 'write', 'settings', 'team'], email='test@ipfabric.io', 
    user_id='1168572704', local=True, sso_provider=None, domains='', custom_scope=True, ldap_id=None)]
    """
    print()

    print(usermgmt.delete_user(user_id=user.user_id))
    """
    [User(username='justin', scope=['read', 'write', 'settings'], email='justin.jeffrey@ipfabric.io', 
        user_id='1108612054', local=True, sso_provider=None, domains='', custom_scope=True, ldap_id=None), 
    User(username='vector', scope=['read', 'write', 'settings'], email='vector@vector.pl', user_id='1083776225', 
        local=True, sso_provider=None, domains='', custom_scope=True, ldap_id=None), ]
    """
    print()