import datetime
import unittest
from unittest.mock import MagicMock, patch

from ipfabric import models


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
            "id": "631ac652-1f72-417f-813f-b8a8c8730157",
            "sites": [{
                "siteName": "BRANCH",
                "uid": "BRANCH",
                "id": "2342875"
            }],
            "errors": [{
                "errorType": "ABMapResultError",
                "count": 1
            }]
        })
        self.assertIsInstance(s, models.Snapshot)
        self.assertIsInstance(s.start, datetime.datetime)

    def test_table(self):
        table = models.Table(client=MagicMock(), endpoint='/network/ip')
        self.assertEqual(table.name, 'ip')

    @patch('ipfabric.IPFClient')
    def test_table_all(self, MockClient):
        table = models.Table(client=MockClient, endpoint='/network/ip')
        MockClient.fetch_all.return_value = list()
        self.assertEqual(table.all(), list())

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
