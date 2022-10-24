import datetime
import unittest

from ipfabric import snapshot_models


class SnapshotModels(unittest.TestCase):
    def test_snapshot(self):
        s = snapshot_models.Snapshot(
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
        self.assertIsInstance(s, snapshot_models.Snapshot)
        self.assertIsInstance(s.start, datetime.datetime)
        self.assertTrue(s.loaded)

