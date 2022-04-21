import unittest
from unittest.mock import MagicMock, patch

from ipfabric.tools import configuration


class Models(unittest.TestCase):
    def test_config(self):
        cfg = configuration.Config(
            id="test",
            sn="test",
            hostname="test",
            hash="test",
            status="test",
            lastCheckAt=1637629200,
            lastChangeAt=1637629200,
        )
        self.assertIsInstance(cfg, configuration.Config)


class DeviceConfigs(unittest.TestCase):
    def setUp(self) -> None:
        self.dc = configuration.DeviceConfigs(MagicMock())

    def test_get_all_configurations(self):
        example = {
            "id": "619d84648eec5403579025bf",
            "sn": "OVAEB9DD0",
            "hostname": "McastRouter2",
            "hash": "be6ae3d00363cd034be33e16e0623c25fe03c3c3",
            "lastChangeAt": 1637712996000,
            "lastCheckAt": 1637712996000,
            "status": "saved",
        }
        self.dc.ipf.fetch_all.return_value = [example]
        cfg = configuration.Config(**example)
        self.assertEqual(self.dc.get_all_configurations(), {"OVAEB9DD0": [cfg]})

    def test_get_all_configurations_device(self):
        example = {
            "id": "619d84648eec5403579025bf",
            "sn": "OVAEB9DD0",
            "hostname": "McastRouter2",
            "hash": "be6ae3d00363cd034be33e16e0623c25fe03c3c3",
            "lastChangeAt": 1637712996000,
            "lastCheckAt": 1637712996000,
            "status": "saved",
        }
        self.dc.ipf.fetch_all.return_value = [example]
        cfg = configuration.Config(**example)
        self.assertEqual(self.dc.get_all_configurations("McastRouter2"), {"OVAEB9DD0": [cfg]})

    def test_get_all_configurations_none(self):
        self.dc.ipf.fetch_all.return_value = []
        self.assertIsNone(self.dc.get_all_configurations("McastRouter2"))

    def test_search_ip(self):
        self.dc.ipf.fetch_all.return_value = [{"ip": "10.0.0.0", "hostname": "test", "sn": "test_sn"}]
        self.assertEqual(self.dc._search_ip("test"), {"hostname": "test", "sn": "test_sn"})

    def test_search_ip_log(self):
        self.dc.ipf.fetch_all.return_value = [{"ip": "10.0.0.0", "hostname": "test", "sn": "test_sn"}]
        self.dc.ipf.inventory.devices.all.return_value = [{"hostname": "test", "taskKey": "task", "sn": "test_sn"}]
        self.assertEqual(self.dc._search_ip("test", log=True), {"hostname": "test", "taskKey": "task", "sn": "test_sn"})

    def test_search_ip_none(self):
        self.dc.ipf.fetch_all.return_value = [{"ip": "10.0.0.0", "hostname": "test"}, None]
        self.assertIsNone(self.dc._search_ip("test")["hostname"])
        self.dc.ipf.fetch_all.return_value = []
        self.assertIsNone(self.dc._search_ip("test")["hostname"])

    @patch("ipfabric.tools.configuration.DeviceConfigs._validate_device")
    @patch("ipfabric.tools.configuration.DeviceConfigs.get_all_configurations")
    def test_get_configuration(self, configs, device):
        device.return_value = {"hostname": "test", "sn": "OVAEB9DD0"}
        configs.return_value = {
            "OVAEB9DD0": [
                configuration.Config(
                    **{
                        "id": "619d84648eec5403579025bf",
                        "sn": "OVAEB9DD0",
                        "hostname": "McastRouter2",
                        "status": "saved",
                        "hash": "be6ae3d00363cd034be33e16e0623c25fe03c3c3",
                        "lastChangeAt": 1637712996000,
                        "lastCheckAt": 1637712996000,
                    }
                )
            ]
        }
        self.dc.ipf.get().text = "CONFIG"
        res = self.dc.get_configuration("test")
        self.assertIsInstance(res, configuration.Config)
        self.assertEqual(res.text, "CONFIG")

    def test_get_configuration_error(self):
        with self.assertRaises(SyntaxError) as err:
            self.dc.get_configuration("test", date="bad")

    def test_get_configuration_device_none(self):
        self.assertIsNone(self.dc.get_configuration("test", date="$prev"))

    @patch("ipfabric.tools.configuration.DeviceConfigs._validate_device")
    def test_get_configuration_cfgs_none(self, device):
        device.return_value = {"hostname": "test", "sn": "test_sn"}
        self.assertIsNone(self.dc.get_configuration("test", date="$prev"))

    @patch("ipfabric.tools.configuration.DeviceConfigs._validate_device")
    @patch("ipfabric.tools.configuration.DeviceConfigs.get_all_configurations")
    @patch("ipfabric.tools.configuration.DeviceConfigs._get_hash")
    def test_get_configuration_hash_none(self, hash, configs, device):
        device.return_value = {"hostname": "test", "sn": "test_sn"}
        configs.return_value = {
            "test_sn": [
                configuration.Config(
                    **{
                        "id": "619d84648eec5403579025bf",
                        "sn": "OVAEB9DD0",
                        "hostname": "McastRouter2",
                        "status": "saved",
                        "hash": "be6ae3d00363cd034be33e16e0623c25fe03c3c3",
                        "lastChangeAt": 1637712996000,
                        "lastCheckAt": 1637712996000,
                    }
                )
            ]
        }
        hash.return_value = None
        self.assertIsNone(self.dc.get_configuration("test"))

    def test_get_hash(self):
        data = [
            {
                "id": "619d83a68eec5403579025b8",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "2ec117a68eba80b1d0d644937cd3ab8d29fcde14",
                "lastChangeAt": 1637712806000,
                "lastCheckAt": 1637712806000,
                "status": "saved",
            },
            {
                "id": "616dffd4c476400368b3fd3c",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "ea732ea21150a0d9f1826bc59b4023dcc609c853",
                "lastChangeAt": 1634598867000,
                "lastCheckAt": 1637626401276,
                "status": "saved",
            },
            {
                "id": "608747d43eb36603a1b48db3",
                "sn": "a22ff67",
                "hostname": "L34R3",
                "hash": "e415efae4fedba53ca13e11a014a1893400cd92f",
                "lastChangeAt": 1619478484000,
                "lastCheckAt": 1625008990651,
                "status": "saved",
            },
            {
                "id": "6070de4cf58e8c66c307c09e",
                "sn": "10.34.255.103",
                "hostname": "L34R3",
                "hash": "0140c1010e60c5efe2eea68fd90282b21aa2ad3b",
                "lastChangeAt": 1618009676000,
                "lastCheckAt": 1619392682986,
                "status": "saved",
            },
        ]
        configs = [configuration.Config(**c) for c in data]
        self.assertEqual(self.dc._get_hash(configs, "$last").config_hash, "2ec117a68eba80b1d0d644937cd3ab8d29fcde14")
        self.assertEqual(self.dc._get_hash(configs, "$prev").config_hash, "ea732ea21150a0d9f1826bc59b4023dcc609c853")
        self.assertEqual(self.dc._get_hash(configs, "$first").config_hash, "0140c1010e60c5efe2eea68fd90282b21aa2ad3b")
        self.assertEqual(
            self.dc._get_hash(configs, ("10/01/2021", 1635625544)).config_hash,
            "ea732ea21150a0d9f1826bc59b4023dcc609c853",
        )
        self.assertIsNone(self.dc._get_hash(configs, ("01/01/2021", "01/01/2021")))

    @patch("ipfabric.tools.configuration.DeviceConfigs._search_ip")
    def test_validate_device_by_ip(self, ip):
        ip.return_value = "test"
        self.assertEqual(self.dc._validate_device("10.0.0.0"), "test")

    def test_validate_device_by_hostname(self):
        self.dc.ipf.inventory.devices.all.return_value = [{"hostname": "test", "taskKey": "task", "sn": "test_sn"}]
        self.assertEqual(self.dc._validate_device("test"), {"hostname": "test", "taskKey": "task", "sn": "test_sn"})

    def test_validate_device_by_hostname_none(self):
        self.dc.ipf.inventory.devices.all.return_value = []
        self.assertIsNone(self.dc._validate_device("test")["hostname"])
        self.dc.ipf.inventory.devices.all.return_value = [None, None]
        self.assertIsNone(self.dc._validate_device("test")["hostname"])

    @patch("ipfabric.tools.configuration.DeviceConfigs._validate_device")
    def test_get_log(self, device):
        device.return_value = {"hostname": "test", "taskKey": "task", "sn": "test_sn"}
        self.dc.ipf.get().text = "LOG"
        self.assertEqual(self.dc.get_log("TEST"), "LOG")

    @patch("ipfabric.tools.configuration.DeviceConfigs._validate_device")
    def test_get_log_device_none(self, device):
        device.return_value = {"hostname": None, "sn": None}
        self.assertIsNone(self.dc.get_log("test"))
