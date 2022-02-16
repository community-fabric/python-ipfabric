import os
import unittest

from pkg_resources import parse_version

import ipfabric.security
from ipfabric import IPFClient

condition = False if os.getenv("IPF_TOKEN", None) and os.getenv("IPF_URL", None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_get_acl(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) >= parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        acls = ipf.security.search_acl_policies()
        self.assertIsInstance(acls, list)

    def test_get_zone(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) >= parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        zones = ipf.security.search_zone_policies()
        self.assertIsInstance(zones, list)

    def test_get_policy(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) >= parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        acl = ipf.security.search_acl_policies()[0]
        policy = ipf.security.get_policy(acl)
        self.assertIsInstance(policy, ipfabric.security.Policy)


if __name__ == "__main__":
    unittest.main()
