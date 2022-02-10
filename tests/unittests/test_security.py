import unittest
from unittest.mock import MagicMock

from ipfabric.security import Security, Policy


class SecurityModel(unittest.TestCase):
    def setUp(self) -> None:
        self.security = Security(client=MagicMock())

    def test_acl(self):
        policies = [
            {"sn": "a48ff83", "hostname": "L72AC26", "name": "CISCO-CWA-URL-REDIRECT-ACL", "defaultAction": "deny"}
        ]
        self.security.client.fetch_all.return_value = policies
        res = self.security.search_acl_policies("L72AC26")
        self.assertEqual(res, policies)

    def test_zone(self):
        policies = [
            {"sn": "a48ff83", "hostname": "L72AC26", "name": "CISCO-CWA-URL-REDIRECT-ACL", "defaultAction": "deny"}
        ]
        self.security.client.fetch_all.return_value = policies
        res = self.security.search_zone_policies("L72AC26")
        self.assertEqual(res, policies)

    def test_policy(self):
        self.security.client.get().json.return_value = dict(hostname="TEST", security=dict())
        res = self.security.get_policy({"sn": "a48ff83"})
        self.assertIsInstance(res, Policy)
        self.assertEqual(res.hostname, "TEST")
