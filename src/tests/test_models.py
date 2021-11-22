import datetime
import unittest
from ipfabric import models
from unittest.mock import MagicMock, patch


class Models(unittest.TestCase):

    def test_snapshot(self):
        s = models.Snapshot(**{
            "loadedSize": "172267939",
            "name": None,
            "note": "",
            "state": "loaded",
            "version": "develop",
            "locked": False,
            "totalDevices": 642,
            "licensedDevCount": 639,
            "status": "done",
            "totalDevCount": 642,
            "tsEnd": 1637156346509,
            "tsStart": 1637154608164,
            "id": "631ac652-1f72-417f-813f-b8a8c8730157"
        })
        self.assertIsInstance(s, models.Snapshot)
        self.assertIsInstance(s.start, datetime.datetime)

    def test_table(self):
        table = models.Table(MagicMock(), '/network/ip')
        self.assertEqual(table.name, 'ip')

    @patch('ipfabric.IPFClient')
    def test_table_all(self, MockClient):
        table = models.Table(MockClient, '/network/ip')
        MockClient.fetch_all.return_value = list()
        self.assertEqual(table.all(), list())

    def test_inventory(self):
        i = models.Inventory(MagicMock())
        self.assertIsInstance(i.vendors, models.Table)
