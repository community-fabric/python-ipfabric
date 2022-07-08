import os
import unittest

from ipfabric import IPFClient

condition = False if os.getenv("IPF_TOKEN", None) and os.getenv("IPF_URL", None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
@unittest.skipIf(True, "Skip till 5.0")  # TODO: Remove
class MyTestCase(unittest.TestCase):
    def test_client(self):
        ipf = IPFClient()
        self.assertIsInstance(ipf, IPFClient)
        self.assertIsInstance(ipf.os_version, str)

    def test_bad_token(self):
        with self.assertRaises(ConnectionRefusedError) as err:
            IPFClient(token="BAD")

    def test_inventory(self):
        ipf = IPFClient()
        devices = ipf.inventory.devices.all(
            filters=dict(vendor=["like", "cisco"]),
            sort=dict(order="desc", column="hostname"),
            reports="/inventory/devices",
        )
        self.assertIsInstance(devices, list)
        self.assertIsInstance(devices[0], dict)

    def test_fetch(self):
        ipf = IPFClient()
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
        ipf = IPFClient()
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
