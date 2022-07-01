import unittest
from unittest.mock import MagicMock

from ipfabric.settings import user_mgmt


def mock_pager(*args):
    if args[0] == "tables/users":
        return [
            {
                "id": "1108612054",
                "isLocal": True,
                "username": "justin",
                "ssoProvider": None,
                "domainSuffixes": "",
                "email": "justin.jeffrey@ipfabric.io",
                "roleNames": ["admin"],
                "timezone": "UTC"
            }
        ]
    else:
        return [{"id": "admin", "name": "admin", "description": "Administrator", "type": "Admin", "isAdmin": True,
                 "isSystem": True}]


class TestUsers(unittest.TestCase):
    def setUp(self) -> None:
        mock = MagicMock()
        mock._ipf_pager.side_effect = mock_pager
        self.usermgmt = user_mgmt.UserMgmt(mock)

    def test_users(self):
        u = self.usermgmt.users[0]
        self.assertIsInstance(u, user_mgmt.User)

    def test_get_users(self):
        u = self.usermgmt.get_users("test")[0]
        self.assertIsInstance(u, user_mgmt.User)

    def test_get_user_by_id(self):
        self.usermgmt.client.get().json.return_value = {
            "id": "1108612054",
            "isLocal": True,
            "username": "justin",
            "ssoProvider": None,
            "domainSuffixes": "",
            "email": "justin.jeffrey@ipfabric.io",
            "roleNames": ["admin"],
            "roleIds": ["admin"],
            "timezone": "UTC"
        }
        u = self.usermgmt.get_user_by_id("1108612054")
        self.assertIsInstance(u, user_mgmt.User)

    def test_add_user(self):
        self.usermgmt.client.post().json.return_value = {
            "id": "1108612054",
            "isLocal": True,
            "username": "justin",
            "ssoProvider": None,
            "domainSuffixes": "",
            "email": "justin.jeffrey@ipfabric.io",
            "roleNames": ["admin"],
            "roleIds": ["admin"],
            "timezone": "UTC"
        }
        u = self.usermgmt.add_user("test", "test", "test1234", ["admin"])
        self.assertIsInstance(u, user_mgmt.User)

    def test_add_user_fail(self):
        with self.assertRaises(SyntaxError) as err:
            self.usermgmt.add_user("test", "test", "test", ["read"])
        with self.assertRaises(SyntaxError) as err:
            self.usermgmt.add_user("test", "test", "test1234", ["hello"])

    def test_delete_user(self):
        u = self.usermgmt.delete_user("test1234")
        self.assertIsInstance(u[0], user_mgmt.User)
