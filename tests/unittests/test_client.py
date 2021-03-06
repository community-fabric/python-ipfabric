import os
import unittest
from unittest.mock import patch

from ipfabric import IPFClient
from ipfabric.client import check_format
from ipfabric.models import Snapshot


class Decorator(unittest.TestCase):
    def test_check_format(self):
        @check_format
        def tester(self, url, **kwargs):
            return (url, kwargs)

        result = tester(None, "/api/v1/networking/ip", filters='{"test": "Hello World"}')
        self.assertEqual(result[0], "networking/ip")
        self.assertEqual(result[1], {"filters": {"test": "Hello World"}})


class FailedClient(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_no_url(self):
        env = dict()
        with self.assertRaises(RuntimeError) as err:
            ipf = IPFClient()

    @patch.dict(os.environ, {}, clear=True)
    def test_no_token(self):
        env = dict()
        with self.assertRaises(RuntimeError) as err:
            ipf = IPFClient(base_url="http://google.com")


class Client(unittest.TestCase):
    @patch("httpx.Client.__init__", return_value=None)
    @patch("httpx.Client.headers")
    @patch("httpx.Client.base_url")
    @patch("ipfabric.IPFClient.fetch_os_version")
    @patch("ipfabric.IPFClient.get_snapshots")
    @patch("ipfabric.models.Inventory")
    def setUp(self, inventory, snaps, os_version, base_url, headers, mock_client):
        snaps.return_value = {
            "$last": Snapshot(
                **{
                    "name": None,
                    "state": "loaded",
                    "locked": False,
                    "totalDevices": 642,
                    "status": "done",
                    "totalDevCount": 642,
                    "licensedDevCount": 600,
                    "tsEnd": 1637156346509,
                    "tsStart": 1637154608164,
                    "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                    "version": "4.1.1",
                    "sites": [{"siteName": "BRANCH", "uid": "BRANCH", "id": "2342875"}],
                    "errors": [{"errorType": "ABMapResultError", "count": 1}],
                }
            )
        }
        mock_client._headers = dict()
        os_version.return_value = "4.2"
        self.ipf = IPFClient(base_url="https://google.com", token='token')

    @patch("httpx.Client.get")
    def test_os(self, get):
        get().is_error = None
        get().json.return_value = dict(version="v5.0.0")
        self.assertEqual(str(self.ipf.fetch_os_version()), "5.0.0")

    @patch("httpx.Client.get")
    def test_os_version_failed(self, get):
        get().is_error = None
        get().json.return_value = dict()
        with self.assertRaises(ConnectionError) as err:
            self.ipf.fetch_os_version()

    @patch("httpx.Client.get")
    def test_os_failed(self, get):
        with self.assertRaises(ConnectionRefusedError) as err:
            self.ipf.fetch_os_version()

    @patch("httpx.Client.get")
    def test_snapshots(self, get):
        get().is_error = None
        get().json.return_value = [
            {
                "name": "Test",
                "state": "loaded",
                "locked": False,
                "totalDevices": 642,
                "status": "done",
                "totalDevCount": 642,
                "licensedDevCount": 600,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                "version": "4.1.1",
                "sites": [{"siteName": "BRANCH", "uid": "BRANCH", "id": "2342875"}],
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
                "note": "Test"
            },
            {
                "name": None,
                "state": "done",
                "locked": True,
                "totalDevices": 642,
                "status": "done",
                "totalDevCount": 642,
                "licensedDevCount": 600,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730158",
                "version": "4.1.1",
                "sites": [{"siteName": "BRANCH", "uid": "BRANCH", "id": "2342875"}],
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
            },
            {
                "name": None,
                "state": "loaded",
                "locked": True,
                "totalDevices": 642,
                "status": "done",
                "totalDevCount": 642,
                "licensedDevCount": 600,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730159",
                "version": "4.1.1",
                "sites": [{"siteName": "BRANCH", "uid": "BRANCH", "id": "2342875"}],
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
            },
        ]
        self.assertIsInstance(self.ipf.get_snapshots()["$last"], Snapshot)
        self.assertEqual(self.ipf.get_snapshots()["$last"].snapshot_id, "631ac652-1f72-417f-813f-b8a8c8730157")
        self.assertEqual(self.ipf.get_snapshots()["$lastLocked"].snapshot_id, "631ac652-1f72-417f-813f-b8a8c8730159")
        self.assertEqual(self.ipf.get_snapshots()["$prev"].snapshot_id, "631ac652-1f72-417f-813f-b8a8c8730159")

    def test_bad_snapshot(self):
        with self.assertRaises(ValueError) as err:
            self.ipf.snapshot_id = "bad"

    @patch("httpx.Client.post")
    def test_fetch(self, post):
        post().json.return_value = {"data": list()}
        self.assertEqual(self.ipf.fetch("test", columns=["*"], filters=dict(a="b"), reports="a", sort=dict(a="b")), [])

    @patch("ipfabric.IPFClient._ipf_pager")
    def test_fetch_all(self, pager):
        pager.return_value = list()
        self.assertEqual(self.ipf.fetch_all("a", columns=["*"], filters=dict(a="b"), reports="1", sort=dict(a="b")), [])

    @patch("httpx.Client.post")
    def test_query(self, post):
        post().json.return_value = {"data": list()}
        self.assertEqual(self.ipf.query("test", '{"data": "hello"}', all=False), [])

    @patch("ipfabric.IPFClient._ipf_pager")
    def test_query_all(self, pager):
        pager.return_value = list()
        self.assertEqual(self.ipf.query("test", '{"data": "hello"}'), [])

    @patch("httpx.Client.post")
    def test_get_columns(self, post):
        post().status_code = 422
        post().json.return_value = {"errors": [{"message": '"hello" [name, id]'}]}
        self.assertEqual(self.ipf._get_columns("test"), ["name", "id"])

    @patch("httpx.Client.post")
    def test_get_columns_failed(self, post):
        post().status_code = 400
        post().raise_for_status.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError) as err:
            self.ipf._get_columns("test")

    @patch("httpx.Client.post")
    def test_ipf_pager(self, post):
        post().json.return_value = {"data": ["hello"], "_meta": {"count": 1}}
        self.assertEqual(self.ipf._ipf_pager("test", dict()), ["hello"])

    @patch("ipfabric.IPFClient.fetch_os_version")
    @patch("ipfabric.IPFClient.get_snapshots")
    def test_update(self, snap, os_v):
        self.ipf.get_snapshots.return_value = 1
        self.ipf.fetch_os_version.return_value = 2
        self.ipf.update()
        self.assertEqual(self.ipf.snapshots, 1)
        self.assertEqual(self.ipf.os_version, 2)
