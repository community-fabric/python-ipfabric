import unittest
from unittest.mock import MagicMock

from ipfabric.settings import users


class TestUsers(unittest.TestCase):
    def test_users(self):
        user = users.Users(MagicMock())
        user.client._ipf_pager.return_value = [{'id': '1108612054', 'isLocal': True, 'username': 'justin',
                                               'ssoProvider': None, 'domainSuffixes': '',
                                               'email': 'justin.jeffrey@ipfabric.io', 'customScope': True,
                                               'scope': ['read', 'write', 'settings']}]
        u = user.users[0]
        self.assertIsInstance(u, users.User)

    def test_get_users(self):
        user = users.Users(MagicMock())
        user.client._ipf_pager.return_value = [{'id': '1108612054', 'isLocal': True, 'username': 'justin',
                                                'ssoProvider': None, 'domainSuffixes': '',
                                                'email': 'justin.jeffrey@ipfabric.io', 'customScope': True,
                                                'scope': ['read', 'write', 'settings']}]
        u = user.get_users('test', '123')[0]
        self.assertIsInstance(u, users.User)
