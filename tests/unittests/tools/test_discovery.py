import unittest
from copy import deepcopy
from unittest.mock import MagicMock

from ipfabric.tools import DiscoveryHistory
from ipfabric.tools.shared import convert_timestamp


class Discovery(unittest.TestCase):
    def setUp(self) -> None:
        self.dh = DiscoveryHistory(MagicMock())
        self.example = [{
            "id": "1282170047",
            "sn": "JMX1426L1FD/admin",
            "hostname": "HWLAB-FW-C5510/admin",
            "loginIp": "10.64.128.9",
            "loginType": "ssh",
            "ts": 1662648437195,
            "username": "admin15",
            "usernameNotes": None
        }]

    def test_get_all_history(self):
        example = deepcopy(self.example)[0]
        example.update({'ts': convert_timestamp(example['ts'], ts_format='ziso')})
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.get_all_history()
        self.assertEqual(history[0], example)

    def test_get_all_history_datetime(self):
        example = deepcopy(self.example)[0]
        example.update({'ts': convert_timestamp(example['ts'])})
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.get_all_history(ts_format='datetime')
        self.assertEqual(history[0], example)

    def test_get_all_history_ts(self):
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.get_all_history(ts_format='int')
        self.assertEqual(history, self.example)

    def test_get_all_history_bad(self):
        self.dh.ipf.fetch_all.return_value = self.example
        with self.assertRaises(SyntaxError) as err:
            self.dh.get_all_history(ts_format='timestamp')

    def test_get_history_date(self):
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.get_history_date('2022-09-30', ts_format='int')
        self.assertEqual(history, self.example)

    def test_get_history_date_range(self):
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.get_history_date(('2022-09-30', '2022-10-10'), ts_format='int')
        self.assertEqual(history, self.example)

    def test_get_snapshot_history(self):
        self.dh.ipf.fetch_all.return_value = self.example
        devices = [
            {
                "sn": "JMX1426L1FD/admin",
                "hostname": "HWLAB-FW-C5510/admin",
                "loginIp": "10.64.128.9",
                "loginType": "ssh",
            },
            {
                "sn": "CJ0196387",
                "hostname": "A_instant_3_53:ae",
                "loginIp": "10.64.128.32",
                "loginType": "lap",
            }
        ]
        self.dh.ipf.inventory.devices.all.return_value = devices
        history, no_history = self.dh.get_snapshot_history('$last')
        self.assertEqual(history[0], self.example[0])
        self.assertEqual(no_history[0], devices[1])

    def test_delete_history_prior_to_ts(self):
        self.dh.ipf.fetch_all.return_value = self.example
        history = self.dh.delete_history_prior_to_ts('2022-09-30')
        self.assertEqual(history, self.example)
