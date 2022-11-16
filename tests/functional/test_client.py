import os
import unittest

from httpx import HTTPStatusError

from ipfabric import IPFClient

os.environ["IPF_VERIFY"] = "false"

condition = False if os.getenv("IPF_TOKEN", None) and os.getenv("IPF_URL", None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_client(self):
        ipf = IPFClient(timeout=15)
        self.assertIsInstance(ipf, IPFClient)
        self.assertIsInstance(str(ipf.os_version), str)

    def test_bad_token(self):
        with self.assertRaises(HTTPStatusError) as err:
            IPFClient(token="BAD")

    def test_inventory(self):
        ipf = IPFClient(timeout=15)
        devices = ipf.inventory.devices.all(
            filters=dict(vendor=["like", "cisco"]),
            sort=dict(order="desc", column="hostname"),
            reports="/inventory/devices",
        )
        self.assertIsInstance(devices, list)
        self.assertIsInstance(devices[0], dict)

    def test_fetch(self):
        ipf = IPFClient(timeout=15)
        devices = ipf.fetch(
            "/tables/inventory/devices",
            columns=["hostname"],
            filters=dict(vendor=["like", "cisco"]),
            sort=dict(order="desc", column="hostname"),
            reports="/inventory/devices",
        )
        self.assertIsInstance(devices, list)
        self.assertIsInstance(devices[0], dict)

    def test_query(self):
        ipf = IPFClient(timeout=15)
        payload = {
            "columns": ["hostname"],
            "filters": {"vendor": ["like", "cisco"]},
            "pagination": {"limit": 23, "start": 0},
            "snapshot": "$last",
            "sort": {"order": "desc", "column": "hostname"},
            "reports": "/inventory/devices",
        }
        devices = ipf.query("/tables/inventory/devices", payload, all=False)
        self.assertIsInstance(devices, list)
        self.assertIsInstance(devices[0], dict)


if __name__ == "__main__":
    unittest.main()
