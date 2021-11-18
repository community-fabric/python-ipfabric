import datetime
import unittest
import client
from models import Snapshot
from unittest.mock import MagicMock, patch
import os


class Decorator(unittest.TestCase):
    def test_check_format(self):
        @client.check_format
        def tester(self, url, **kwargs):
            return (url, kwargs)

        result = tester(None, '/api/v1/networking/ip', filters='{"test": "Hello World"}')
        self.assertEqual(result[0], 'networking/ip')
        self.assertEqual(result[1], {'filters': {'test': 'Hello World'}})


class FailedClient(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_no_url(self):
        env = dict()
        with self.assertRaises(RuntimeError) as err:
            ipf = client.IPFClient()

    @patch.dict(os.environ, {}, clear=True)
    def test_no_token(self):
        env = dict()
        with self.assertRaises(RuntimeError) as err:
            ipf = client.IPFClient('http://google.com')



class Client(unittest.TestCase):
    @patch("client.Client.__init__", return_value=None)
    @patch("client.Client.headers")
    @patch("client.Client.base_url")
    @patch("client.IPFClient.fetch_os_version")
    @patch("client.IPFClient.get_snapshots")
    @patch("models.Inventory")
    def setUp(self, inventory, snaps, os, base_url, headers, mock_client):
        snaps.return_value = {"$last": Snapshot(**{
            "name": None,
            "state": "loaded",
            "locked": False,
            "totalDevices": 642,
            "status": "done",
            "totalDevCount": 642,
            "tsEnd": 1637156346509,
            "tsStart": 1637154608164,
            "id": "631ac652-1f72-417f-813f-b8a8c8730157"
        })}
        mock_client._headers = dict()
        self.ipf = client.IPFClient('google.com', 'token')


    @patch("client.IPFClient.get")
    def test_os(self, get):
        get().is_error = None
        get().json.return_value = dict(version="test")
        self.assertEqual(self.ipf.fetch_os_version(), 'test')

    @patch("client.IPFClient.get")
    def test_os_version_failed(self, get):
        get().is_error = None
        get().json.return_value = dict()
        with self.assertRaises(ConnectionError) as err:
            self.ipf.fetch_os_version()

    @patch("client.IPFClient.get")
    def test_os_failed(self, get):
        with self.assertRaises(ConnectionRefusedError) as err:
            self.ipf.fetch_os_version()

    @patch("client.IPFClient.get")
    def test_snapshots(self, get):
        get().is_error = None
        get().json.return_value = [{
            "name": None,
            "state": "loaded",
            "locked": False,
            "totalDevices": 642,
            "status": "done",
            "totalDevCount": 642,
            "tsEnd": 1637156346509,
            "tsStart": 1637154608164,
            "id": "631ac652-1f72-417f-813f-b8a8c8730157"
        }, {
            "name": None,
            "state": "done",
            "locked": True,
            "totalDevices": 642,
            "status": "done",
            "totalDevCount": 642,
            "tsEnd": 1637156346509,
            "tsStart": 1637154608164,
            "id": "631ac652-1f72-417f-813f-b8a8c8730158"
        }, {
            "name": None,
            "state": "loaded",
            "locked": True,
            "totalDevices": 642,
            "status": "done",
            "totalDevCount": 642,
            "tsEnd": 1637156346509,
            "tsStart": 1637154608164,
            "id": "631ac652-1f72-417f-813f-b8a8c8730159"
        }]
        self.assertIsInstance(self.ipf.get_snapshots()["$last"], Snapshot)
        self.assertEqual(self.ipf.get_snapshots()["$last"].id, "631ac652-1f72-417f-813f-b8a8c8730157")
        self.assertEqual(self.ipf.get_snapshots()["$lastLocked"].id, "631ac652-1f72-417f-813f-b8a8c8730159")
        self.assertEqual(self.ipf.get_snapshots()["$prev"].id, "631ac652-1f72-417f-813f-b8a8c8730159")

    def test_bad_snapshot(self):
        with self.assertRaises(ValueError) as err:
            self.ipf.snapshot_id = 'bad'

    @patch("client.IPFClient.post")
    def test_fetch(self, post):
        post().json.return_value = {"data": list()}
        self.assertEqual(self.ipf.fetch('test', columns=['*'], filters=dict(a="b"), reports='hello'), [])

    @patch("client.IPFClient._ipf_pager")
    def test_fetch_all(self, pager):
        pager.return_value = list()
        self.assertEqual(self.ipf.fetch_all('test', columns=['*'], filters=dict(a="b"), reports='hello'), [])

    @patch("client.IPFClient.post")
    def test_query(self, post):
        post().json.return_value = {"data": list()}
        self.assertEqual(self.ipf.query('test', '{"data": "hello"}', all=False), [])

    @patch("client.IPFClient._ipf_pager")
    def test_query_all(self, pager):
        pager.return_value = list()
        self.assertEqual(self.ipf.query('test', '{"data": "hello"}'), [])

    @patch("client.IPFClient.post")
    def test_get_columns(self, post):
        post().status_code = 422
        post().json.return_value = {"errors": [{"message": '"hello" [name, id]'}]}
        self.assertEqual(self.ipf._get_columns('test'), ["name", "id"])

    @patch("client.IPFClient.post")
    def test_get_columns_failed(self, post):
        post().status_code = 400
        post().raise_for_status.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError) as err:
            self.ipf._get_columns('test')

    @patch("client.IPFClient.post")
    def test_ipf_pager(self, post):
        post().json.return_value = {"data": ["hello"], "_meta": {"count": 1}}
        self.assertEqual(self.ipf._ipf_pager('test', dict()), ["hello"])
