import os
import unittest
from unittest.mock import patch

from packaging.version import parse

from ipfabric import IPFClient
from ipfabric.client import check_format
from ipfabric.settings.user_mgmt import User
from ipfabric.snapshot_models import Snapshot


class Decorator(unittest.TestCase):
    def test_check_format(self):
        @check_format
        def tester(self, url, **kwargs):
            return (url, kwargs)

        tests = [
            ('v5/tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('v5.0/tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('api/v5/tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('https://demo3.ipfabric.io/api/v5.0/tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('/tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('tables/addressing/ipv6-neighbors', "tables/addressing/ipv6-neighbors"),
            ('v5/tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
            ('v5.0/tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
            ('api/v5/tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
            ('https://demo3.ipfabric.io/api/v5.0/tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
            ('/tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
            ('tables/routing/protocols/ospf-v3/neighbors', "tables/routing/protocols/ospf-v3/neighbors"),
        ]

        for test in tests:
            result = tester(None, test[0], filters='{"test": "Hello World"}')
            self.assertEqual(result[0], test[1], msg=test[0])
            self.assertEqual(result[1], {"filters": {"test": "Hello World"}})


class FailedClient(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_no_url(self):
        env = dict()
        with self.assertRaises(RuntimeError) as err:
            ipf = IPFClient()

    @patch.dict(os.environ, {}, clear=True)
    @patch('dotenv.load_dotenv', return_value=None)
    @patch("ipfabric.IPFClient.check_version")
    def test_no_token(self, version, dotenv):
        env = dict()
        version.return_value = 'v5', parse('v5.0.1')
        with self.assertRaises(RuntimeError) as err:
            ipf = IPFClient(base_url="http://google.com")


class Client(unittest.TestCase):
    @patch("httpx.Client.__init__", return_value=None)
    @patch("httpx.Client.headers")
    @patch("ipfabric.IPFClient.get_user")
    @patch("ipfabric.IPFClient.check_version")
    @patch("ipfabric.IPFClient.get_snapshots")
    @patch("ipfabric.models.Inventory")
    def setUp(self, inventory, snaps, check_version, get_user,  headers, mock_client):
        snaps.return_value = {
            "$last": Snapshot(
                **{
                    "name": None,
                    "locked": False,
                    "totalDevices": 642,
                    "status": "done",
                    "totalDevCount": 642,
                    "licensedDevCount": 600,
                    "tsEnd": 1637156346509,
                    "tsStart": 1637154608164,
                    "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                    "version": "4.1.1",
                    "initialVersion": "3.8.0",
                    "sites": ["BRANCH"],
                    "errors": [{"errorType": "ABMapResultError", "count": 1}],
                    "loadedSize": 10,
                    "unloadedSize": 0,
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
        }
        mock_client._headers = dict()
        check_version.return_value = ("v5", "v5.0.1")
        self.ipf = IPFClient(base_url='https://demo.ipfabric.io', token='token')
        self.ipf.user = User(username='admin', id='admin', roleIds=['admin'], timezone='UTC')

    @patch("httpx.Client.get")
    def test_get_user(self, get):
        get().is_error = None
        get().json.return_value = {"email": "admin@ipfabric.io", "isLocal": True, "timezone": "UTC",
                                   "username": "admin", "active": True, "ldapId": None, "id": "863",
                                   "roleIds": ["admin"]}
        user = self.ipf.get_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'admin')

    @patch("httpx.Client.get")
    def test_check_version(self, get):
        get().is_error = None
        get().json.return_value = {"apiVersion": "v5.1", "releaseVersion": "5.0.1+10"}
        api_version, os_version = self.ipf.check_version('v5.0', 'TEST')
        self.assertEqual(api_version, 'v5.0')
        self.assertEqual(str(os_version), "5.0.1+10")

    @patch('ipfabric.api.importlib_metadata')
    @patch("httpx.Client.get")
    def test_check_version_no_version(self, get, meta):
        meta.version.return_value = 'v6.0.0'
        get().is_error = None
        get().json.return_value = {"apiVersion": "v6.1", "releaseVersion": "6.0.1+10"}
        api_version, os_version = self.ipf.check_version(None, 'TEST')
        self.assertEqual(api_version, f"v6.0")
        self.assertEqual(str(os_version), "6.0.1+10")

    @patch("httpx.Client.get")
    def test_check_version_api_gt_os(self, get):
        get().is_error = None
        get().json.return_value = {"apiVersion": "v5.1", "releaseVersion": "5.0.1+10"}
        api_version, os_version = self.ipf.check_version('v5.2', 'TEST')
        self.assertEqual(api_version, 'v5.1')
        self.assertEqual(str(os_version), "5.0.1+10")

    @patch("httpx.Client.get")
    def test_check_version_os_gt_api(self, get):
        get().is_error = None
        get().json.return_value = {"apiVersion": "v6.1", "releaseVersion": "5.0.1+10"}
        with self.assertRaises(RuntimeError) as err:
            self.ipf.check_version('v5.2', 'TEST')

    @patch("httpx.Client.get")
    def test_check_version_v1(self, get):
        get().is_error = None
        get().json.return_value = {"apiVersion": "v5.1", "releaseVersion": "5.0.1+10"}
        with self.assertRaises(RuntimeError) as err:
            self.ipf.check_version('v1', 'TEST')

    @patch("httpx.Client.get")
    def test_check_short_version(self, get):
        get().is_error = None
        get().json.return_value = {"apiVersion": "v5.1", "releaseVersion": "5.0.1+10"}
        api_version, os_version = self.ipf.check_version('v6', 'TEST')
        self.assertEqual(api_version, 'v5')
        self.assertEqual(str(os_version), "5.0.1+10")

    @patch('ipfabric.snapshot_models.Snapshot.get_assurance_engine_settings')
    @patch('ipfabric.api.IPFabricAPI._ipf_pager')
    @patch("httpx.Client.get")
    def test_snapshots(self, get, pager, ae_settings):
        pager.return_value = [
            {
                "name": "Test",
                "status": "done",
                "locked": False,
                "totalDevices": 642,
                "totalDevCount": 642,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                "sites": ["BRANCH"],
                "note": "Test",
                "loadedSize": 50,
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
            },
            {
                "name": None,
                "status": "unloaded",
                "locked": True,
                "totalDevices": 642,
                "totalDevCount": 642,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730158",
                "sites": ["BRANCH"],
                "unloadedSize": 10,
                "loadedSize": 50,
                "fromArchive": True,
                "loading": False,
                "finishStatus": "done",
                "userCount": 10,
                "interfaceActiveCount": 10,
                "interfaceCount": 10,
                "interfaceEdgeCount": 10,
                "deviceAddedCount": 10,
                "deviceRemovedCount": 10,
            },
            {
                "name": None,
                "status": "done",
                "locked": True,
                "totalDevices": 642,
                "totalDevCount": 642,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608159,
                "id": "631ac652-1f72-417f-813f-b8a8c8730159",
                "sites": ["BRANCH"],
                "unloadedSize": 10,
                "loadedSize": 50,
                "fromArchive": True,
                "loading": False,
                "finishStatus": "done",
                "userCount": 10,
                "interfaceActiveCount": 10,
                "interfaceCount": 10,
                "interfaceEdgeCount": 10,
                "deviceAddedCount": 10,
                "deviceRemovedCount": 10,
            },
        ]
        get().is_error = None
        get().json.return_value = [
            {
                "licensedDevCount": 600,
                "id": "631ac652-1f72-417f-813f-b8a8c8730157",
                "version": "4.1.1",
                "initialVersion": "4.0.0",
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
            },
            {
                "licensedDevCount": 600,
                "id": "631ac652-1f72-417f-813f-b8a8c8730158",
                "version": "4.1.1",
                "initialVersion": "4.0.0",
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
            },
            {
                "licensedDevCount": 600,
                "id": "631ac652-1f72-417f-813f-b8a8c8730159",
                "version": "4.1.1",
                "initialVersion": "4.0.0",
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
        self.assertEqual(self.ipf.query("test", '{"data": "hello"}', get_all=False), [])

    @patch("ipfabric.IPFClient._ipf_pager")
    def test_query_all(self, pager):
        pager.return_value = list()
        self.assertEqual(self.ipf.query("test", '{"data": "hello"}'), [])

    @patch("httpx.Client.post")
    def test_get_columns(self, post):
        post().status_code = 422
        post().json.return_value = {"errors": [{"message": '"hello" [name, id]'}]}
        self.assertEqual(self.ipf.get_columns("test"), ["name", "id"])

    @patch("httpx.Client.post")
    def test_get_columns_failed(self, post):
        post().status_code = 400
        post().raise_for_status.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError) as err:
            self.ipf.get_columns("test")

    @patch("httpx.Client.post")
    def test_ipf_pager(self, post):
        post().json.return_value = {"data": ["hello", "world"], "_meta": {"count": 2}}
        self.assertEqual(self.ipf._ipf_pager("test", dict(), limit=3), ["hello", "world"])

    @patch("ipfabric.IPFClient.get_snapshots")
    def test_update(self, snap):
        self.ipf.get_snapshots.return_value = 1
        self.ipf.update()
        self.assertEqual(self.ipf.snapshots, 1)

    @patch("httpx.Client.post")
    def test_ipf_count(self, post):
        post().json.return_value = {"data": ["hello"], "_meta": {"count": 1}}
        self.assertEqual(self.ipf.get_count('test'), 1)

    def test_filter(self):
        self.ipf.attribute_filters = {"FLOOR": ["12"]}
        self.assertEqual(self.ipf.attribute_filters, {"FLOOR": ["12"]})

    @patch("ipfabric.IPFClient.update")
    def test_unloaded_snapshots(self, update):
        self.assertEqual(self.ipf.unloaded_snapshots, {})

    def test_get_snapshot(self):
        self.assertEqual(self.ipf.get_snapshot('$last'), self.ipf.snapshots['$last'])

    @patch('ipfabric.api.IPFabricAPI._ipf_pager')
    @patch("httpx.Client.get")
    def test_get_snapshot_from_server(self, get, pager):
        pager.return_value = [
            {
                "name": None,
                "status": "unloaded",
                "locked": True,
                "totalDevices": 642,
                "totalDevCount": 642,
                "tsEnd": 1637156346509,
                "tsStart": 1637154608164,
                "id": "631ac652-1f72-417f-813f-b8a8c8730158",
                "sites": ["BRANCH"],
                "unloadedSize": 10,
                "loadedSize": 50,
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
        ]
        get().is_error = None
        get().json.return_value = [
            {
                "licensedDevCount": 600,
                "id": "631ac652-1f72-417f-813f-b8a8c8730158",
                "version": "4.1.1",
                "initialVersion": "4.0.0",
                "errors": [{"errorType": "ABMapResultError", "count": 1}],
            }
        ]
        self.assertEqual(self.ipf.get_snapshot('631ac652-1f72-417f-813f-b8a8c8730158').snapshot_id,
                         '631ac652-1f72-417f-813f-b8a8c8730158')
