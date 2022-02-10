import unittest
from unittest.mock import MagicMock

from ipfabric.settings import user_mgmt


class TestUsers(unittest.TestCase):
    def setUp(self) -> None:
        mock = MagicMock()
        mock._ipf_pager.return_value = [
            {
                "id": "1108612054",
                "isLocal": True,
                "username": "justin",
                "ssoProvider": None,
                "domainSuffixes": "",
                "email": "justin.jeffrey@ipfabric.io",
                "customScope": True,
                "scope": ["read", "write", "settings"],
            }
        ]
        mock.get().json.return_value = {
            "id": "1108612054",
            "isLocal": True,
            "username": "justin",
            "ssoProvider": None,
            "domainSuffixes": "",
            "email": "justin.jeffrey@ipfabric.io",
            "customScope": True,
            "scope": ["read", "write", "settings"],
        }
        self.usermgmt = user_mgmt.UserMgmt(mock)

    def test_users(self):
        u = self.usermgmt.users[0]
        self.assertIsInstance(u, user_mgmt.User)

    def test_get_users(self):
        u = self.usermgmt.get_users("test")[0]
        self.assertIsInstance(u, user_mgmt.User)

    def test_get_user_by_id(self):
        u = self.usermgmt.get_user_by_id("1108612054")
        self.assertIsInstance(u, user_mgmt.User)

    def test_add_user(self):
        self.usermgmt.client.post().json.return_value = {"id": 1}
        u = self.usermgmt.add_user("test", "test", "test1234", ["read"])
        self.assertIsInstance(u, user_mgmt.User)

    def test_add_user_fail(self):
        with self.assertRaises(SyntaxError) as err:
            self.usermgmt.add_user("test", "test", "test", ["read"])
        with self.assertRaises(SyntaxError) as err:
            self.usermgmt.add_user("test", "test", "test1234", ["hello"])

    def test_delete_user(self):
        u = self.usermgmt.delete_user("test1234")
        self.assertIsInstance(u[0], user_mgmt.User)
