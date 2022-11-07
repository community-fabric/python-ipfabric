import unittest
from unittest.mock import MagicMock, patch

from ipfabric import models


class Models(unittest.TestCase):
    def test_table(self):
        table = models.Table(client=MagicMock(), endpoint="/network/ip")
        self.assertEqual(table.name, "ip")

    @patch("ipfabric.IPFClient")
    def test_table_all(self, MockClient):
        table = models.Table(client=MockClient, endpoint="/network/ip")
        MockClient.fetch_all.return_value = list()
        self.assertEqual(table.all(), list())

    @patch("ipfabric.IPFClient")
    def test_table_fetch(self, MockClient):
        table = models.Table(client=MockClient, endpoint="/network/ip")
        MockClient.fetch.return_value = list()
        self.assertEqual(table.fetch(), list())

    @patch("ipfabric.IPFClient")
    def test_table_count(self, MockClient):
        table = models.Table(client=MockClient, endpoint="/network/ip")
        MockClient.get_count.return_value = 1
        self.assertEqual(table.count(), 1)

    def test_inventory(self):
        i = models.Inventory(client=MagicMock())
        self.assertIsInstance(i.vendors, models.Table)
        self.assertIsInstance(i.sites, models.Table)
        self.assertIsInstance(i.devices, models.Table)
        self.assertIsInstance(i.platforms, models.Table)
        self.assertIsInstance(i.families, models.Table)
        self.assertIsInstance(i.pn, models.Table)
        self.assertIsInstance(i.interfaces, models.Table)
        self.assertIsInstance(i.models, models.Table)
