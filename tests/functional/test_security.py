import os
import unittest

import ipfabric.security
from ipfabric import IPFClient

condition = False if os.getenv('IPF_TOKEN', None) and os.getenv('IPF_URL', None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_get_acl(self):
        ipf = IPFClient()
        acls = ipf.security.search_acl_policies()
        self.assertIsInstance(acls, list)

    def test_get_zone(self):
        ipf = IPFClient()
        zones = ipf.security.search_zone_policies()
        self.assertIsInstance(zones, list)

    def test_get_policy(self):
        ipf = IPFClient()
        acl = ipf.security.search_acl_policies()[0]
        policy = ipf.security.get_policy(acl)
        self.assertIsInstance(policy, ipfabric.security.Policy)


if __name__ == '__main__':
    unittest.main()
