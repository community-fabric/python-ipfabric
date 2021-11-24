import unittest
from unittest.mock import MagicMock, patch

from ipfabric.tools import configuration


class Models(unittest.TestCase):
    def test_config(self):
        cfg = configuration.Config(_id='test', sn='test', hostname='test', hash='test', status='test',
                                   lastCheck=1637629200, lastChange=1637629200)
        self.assertIsInstance(cfg, configuration.Config)

    def test_result(self):
        cfg = configuration.Result(timestamp=1637629200, text='CONFIG')
        self.assertIsInstance(cfg, configuration.Result)


class DeviceConfigs(unittest.TestCase):
    @patch('ipfabric.tools.configuration.DeviceConfigs._get_managed_ips')
    @patch('ipfabric.tools.configuration.DeviceConfigs._get_all_configurations')
    def setUp(self, config, ips) -> None:
        self.dc = configuration.DeviceConfigs(MagicMock())
        self.dc.configs = {
            'test': [configuration.Config(_id='test', sn='test', hostname='test', hash='test',  status='test',
                                          lastCheck=1637629200, lastChange=1637629200)]
        }
        self.dc.managed_ip = {'10.0.0.1': 'test'}

    def test_validate_device(self):
        self.assertEqual(self.dc._validate_device('test'), 'test')
        self.assertEqual(self.dc._validate_device('10.0.0.1'), 'test')

    def test_validate_device_failed(self):
        self.assertIsNone(self.dc._validate_device('bad'))
        self.assertIsNone(self.dc._validate_device('10.0.0.2'))

    def test_get_managed_ips(self):
        self.dc.client.fetch_all.return_value = [{'ip': '10.46.120.7', 'hostname': 'L46DR7'}]
        self.dc._get_managed_ips()
        self.assertEqual(self.dc.managed_ip, {'10.46.120.7': 'L46DR7'})

    def test_get_all_configurations(self):
        example = {'_id': '619d84648eec5403579025bf', 'sn': 'OVAEB9DD0', 'hostname': 'McastRouter2',
                   'hash': 'be6ae3d00363cd034be33e16e0623c25fe03c3c3', 'lastChange': 1637712996000,
                   'lastCheck': 1637712996000, 'status': 'saved'}
        self.dc.client.fetch_all.return_value = [example]
        cfg = configuration.Config(**example)
        self.dc._get_all_configurations()
        self.assertEqual(self.dc.configs, {'McastRouter2': [cfg]})

    def test_get_configuration(self):
        self.dc.client.get().text = 'CONFIG'
        res = self.dc.get_configuration('test')
        self.assertIsInstance(res, configuration.Result)
        self.assertEqual(res.text, 'CONFIG')

    def test_get_configuration_error(self):
        with self.assertRaises(SyntaxError) as err:
            res = self.dc.get_configuration('test', date='bad')

    def test_get_configuration_none(self):
        self.assertIsNone(self.dc.get_configuration('test', date='$prev'))

    def test_get_hash(self):
        data = [
            {
                "_id": "619d83a68eec5403579025b8",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "2ec117a68eba80b1d0d644937cd3ab8d29fcde14",
                "lastChange": 1637712806000,
                "lastCheck": 1637712806000,
                "status": "saved"
            }, {
                "_id": "616dffd4c476400368b3fd3c",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "ea732ea21150a0d9f1826bc59b4023dcc609c853",
                "lastChange": 1634598867000,
                "lastCheck": 1637626401276,
                "status": "saved"
            }, {
                "_id": "608747d43eb36603a1b48db3",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "e415efae4fedba53ca13e11a014a1893400cd92f",
                "lastChange": 1619478484000,
                "lastCheck": 1625008990651,
                "status": "saved"
            }, {
                "_id": "6070de4cf58e8c66c307c09e",
                "sn": "10.34.255.103",
                "hostname": "L34R3",
                "hash": "0140c1010e60c5efe2eea68fd90282b21aa2ad3b",
                "lastChange": 1618009676000,
                "lastCheck": 1619392682986,
                "status": "saved"
            }
        ]
        configs = [configuration.Config(**c) for c in data]
        self.assertEqual(self.dc._get_hash(configs, "$last")[0], "2ec117a68eba80b1d0d644937cd3ab8d29fcde14")
        self.assertEqual(self.dc._get_hash(configs, "$prev")[0], "ea732ea21150a0d9f1826bc59b4023dcc609c853")
        self.assertEqual(self.dc._get_hash(configs, "$first")[0], "0140c1010e60c5efe2eea68fd90282b21aa2ad3b")
        self.assertEqual(self.dc._get_hash(configs, ('10/01/2021', 1635625544))[0], "ea732ea21150a0d9f1826bc59b4023dcc609c853")
