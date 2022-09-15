import unittest
from unittest.mock import MagicMock

from ipfabric.settings import APIToken


class TestToken(unittest.TestCase):
    def setUp(self) -> None:
        self.token = APIToken(MagicMock())
        self.token_data = {
            "description": "Justin",
            "expires": None,
            "lastUsed": 1638555602222,
            "scope": ["read"],
            "usage": 9585,
            "maxScope": ["read", "write", "settings"],
            "id": "1158890326",
            "userId": "1108612054",
            "username": "justin",
            "isExpired": False,
        }
        self.token.client.get().json.return_value = [self.token_data]
        self.token.client.post().json.return_value = self.token_data

    # def test_add_token(self):
    #     res = self.token.add_token("TEST", ["read"], token="LONGTOKEN")
    #     self.assertEqual(res["token"], "LONGTOKEN")
    #
    # def test_add_random_token(self):
    #     res = self.token.add_token("TEST", ["read"])
    #     self.assertIsInstance(res["token"], str)
    #     self.assertEqual(len(res["token"]), 32)
    #
    # def test_add_short_token(self):
    #     with self.assertRaises(SyntaxError) as err:
    #         self.token.add_token("TEST", ["read"], token="TOKEN")
    #
    # def test_add_bad_scope(self):
    #     with self.assertRaises(SyntaxError) as err:
    #         self.token.add_token("TEST", ["BAD"])

    def test_delete_token(self):
        res = self.token.delete_token("LONGTOKEN")
        self.assertEqual(res, [self.token_data])
