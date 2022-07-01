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
    username='test' email='test@test.ipfabric.io' user_id='50632669251' local=True sso_provider=None domains='' 
    role_names=['admin'] role_ids=['admin'] ldap_id=None timezone='UTC'
    """
    print()

    user = usermgmt.add_user(username='Test', email='test@ipfabric.io', password='8characters',
                             roles=[usermgmt.roles[0].role_id])
    print(user)
    """
    username='Test' email='test@ipfabric.io' user_id='52914335501' local=True sso_provider=None domains=None 
    role_names=['Network engineer'] role_ids=['Network engineer'] ldap_id=None timezone='UTC'

    """
    print()

    print(usermgmt.get_user_by_id(user_id=user.user_id))
    """
    username='Test' email='test@ipfabric.io' user_id='52914335501' local=True sso_provider=None domains=None 
    role_names=['Network engineer'] role_ids=['Network engineer'] ldap_id=None timezone='UTC'
    """
    print()

    print(usermgmt.get_users(username=user.username))
    """
    [User(username='Test', email='test@ipfabric.io', user_id='52914337160', local=True, sso_provider=None, domains='', 
    role_names=['Network engineer'], role_ids=['Network engineer'], ldap_id=None, timezone='UTC')]
    """
    print()

    print(usermgmt.delete_user(user_id=user.user_id))

    print()