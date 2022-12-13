import datetime
import unittest
from unittest.mock import MagicMock

from ipfabric import snapshot_models


class SnapshotModels(unittest.TestCase):
    def setUp(self) -> None:
        self.snap = snapshot_models.Snapshot(
            **{
                "loadedSize": "172267939",
                "name": None,
                "note": "",
                "version": "develop",
                "locked": False,
                "totalDevices": 642,
                "licensedDevCount": 639,
                "status": "done",
                "totalDevCount": 642,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                "sites": ["BRANCH"],
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
                "unloadedSize": 10,
                "fromArchive": True,
                "loading": False,
                "finishStatus": "done",
                "userCount": 10,
                "interfaceActiveCount": 10,
                "interfaceCount": 10,
                "interfaceEdgeCount": 10,
                "deviceAddedCount": 10,
                "deviceRemovedCount": 10,

            }
        )

    def test_snapshot(self):
        self.assertIsInstance(self.snap, snapshot_models.Snapshot)
        self.assertIsInstance(self.snap.start, datetime.datetime)
        self.assertTrue(self.snap.loaded)

    def test_lock(self):
        self.assertTrue(self.snap.lock(MagicMock()))
        self.assertTrue(self.snap.lock(MagicMock()))

    def test_lock_false(self):
        self.snap.status = 'unloaded'
        self.assertFalse(self.snap.lock(MagicMock()))

    def test_unlock(self):
        self.snap.locked = True
        self.assertTrue(self.snap.unlock(MagicMock()))
        self.assertTrue(self.snap.unlock(MagicMock()))

    def test_unlock_unloaded(self):
        self.snap.status = 'unloaded'
        self.assertTrue(self.snap.unlock(MagicMock()))

    def test_unload(self):
        self.assertTrue(self.snap.unload(MagicMock()))
        self.assertTrue(self.snap.unload(MagicMock()))

    def test_load(self):
        self.assertTrue(self.snap.load(MagicMock(), wait_for_load=False, wait_for_assurance=False))
        self.snap.status = 'unloaded'
        self.assertTrue(self.snap.load(MagicMock(), wait_for_load=False, wait_for_assurance=False))

    def test_attributes(self):
        ipf = MagicMock()
        ipf.fetch_all.return_value = [{'name': 'siteName', 'value': 'TEST', 'sn': 'TEST', 'id': '1'}]
        self.assertEqual(self.snap.attributes(ipf)[0]['id'], '1')
