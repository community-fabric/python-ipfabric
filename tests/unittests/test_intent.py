import unittest
from unittest.mock import MagicMock, patch

from ipfabric import intent_models as imodels
from ipfabric.intent import Intent


class TestIntent(unittest.TestCase):
    def setUp(self) -> None:
        self.i = Intent(MagicMock())
        self.i_json = {
            "groups": [{"id": "320668119", "custom": True, "name": "Neighborship compliance"}],
            "apiEndpoint": "/v1/tables/neighbors/unidirectional",
            "checks": {},
            "column": "localHost",
            "custom": False,
            "defaultColor": 10,
            "descriptions": {
                "checks": {"0": "", "10": "Unidirectional CDP or LLDP sessions.", "20": "", "30": ""},
                "general": "Detects unidirectional Cisco Discovery Protocol (CDP) or Link-Layer Discovery Protocol (LLDP) sessions.\n",
            },
            "name": "CDP/LLDP unidirectional",
            "webEndpoint": "/technology/cdp-lldp/unidirectional-neighbors",
            "id": "320633253",
            "status": 1,
            "result": {"checks": {"10": 21, "20": 10}, "count": 21},
        }
        self.g_json = {
            "children": [
                {"id": "322166922", "weight": 1},
                {"id": "322316649", "weight": 1},
                {"id": "322316648", "weight": 1},
                {"id": "307633865", "weight": 1},
                {"id": "307632121", "weight": 1},
                {"id": "624588369", "weight": 1},
            ],
            "custom": False,
            "name": "First Hop Redundancy Protocol (FHRP)",
            "id": "320668116",
        }

    def test_get_intent_checks(self):
        self.i.client.get().json.return_value = [self.i_json]
        intents = self.i.get_intent_checks()
        self.assertIsInstance(intents[0], imodels.IntentCheck)

    def test_get_groups(self):
        self.i.client.get().json.return_value = [self.g_json]
        groups = self.i.get_groups()
        self.assertIsInstance(groups[0], imodels.Group)

    @patch("ipfabric.intent.Intent.get_intent_checks", return_value=[1])
    @patch("ipfabric.intent.Intent.get_groups", return_value=[2])
    def test_load_intent(self, mock_g, mock_i):
        self.i.load_intent()
        self.assertEqual(self.i.intent_checks, [1])
        self.assertEqual(self.i.groups, [2])

    @patch("ipfabric.intent.Intent.get_intent_checks")
    @patch("ipfabric.intent.Intent.get_groups", return_value=[2])
    def test_custom_builtin(self, mock_g, mock_i):
        mock_i.return_value = [imodels.IntentCheck(**self.i_json)]
        self.assertEqual(self.i.builtin[0].name, "CDP/LLDP unidirectional")
        self.i.intent_checks = None
        self.i_json["custom"] = True
        mock_i.return_value = [imodels.IntentCheck(**self.i_json)]
        self.assertEqual(self.i.custom[0].name, "CDP/LLDP unidirectional")

    @patch("ipfabric.intent.Intent.get_intent_checks")
    @patch("ipfabric.intent.Intent.get_groups", return_value=[2])
    def test_intent_by(self, mock_g, mock_i):
        mock_i.return_value = [imodels.IntentCheck(**self.i_json)]
        self.assertEqual(list(self.i.intent_by_id.keys()), ["320633253"])
        self.i.intent_checks = None
        self.assertEqual(list(self.i.intent_by_name.keys()), ["CDP/LLDP unidirectional"])

    @patch("ipfabric.intent.Intent.get_intent_checks", return_value=[2])
    @patch("ipfabric.intent.Intent.get_groups")
    def test_group_by(self, mock_g, mock_i):
        mock_g.return_value = [imodels.Group(**self.g_json)]
        self.assertEqual(list(self.i.group_by_id.keys()), ["320668116"])
        self.i.groups = None
        self.assertEqual(list(self.i.group_by_name.keys()), ["First Hop Redundancy Protocol (FHRP)"])

    def test_get_result(self):
        self.i.client.fetch_all.return_value = ["TEST"]
        r = self.i.get_results(imodels.IntentCheck(**self.i_json), "blue")
        self.assertEqual(r, ["TEST"])

    @patch("ipfabric.intent.Intent.get_intent_checks")
    def test_compare(self, mock_i):
        self.i.intent_checks = [imodels.IntentCheck(**self.i_json)]
        self.i_json["result"]["checks"]["count"] = 50
        self.i_json["result"]["checks"]["10"] = 22
        self.i_json["result"]["checks"]["20"] = 5
        self.i_json["result"]["checks"]["30"] = 100
        mock_i.return_value = [imodels.IntentCheck(**self.i_json)]
        comp = self.i.compare_snapshot("$last")
        data = [
            {
                "name": "CDP/LLDP unidirectional",
                "id": "320633253",
                "check": "total",
                "loaded_snapshot": 21,
                "compare_snapshot": 21,
                "diff": 0,
            },
            {
                "name": "CDP/LLDP unidirectional",
                "id": "320633253",
                "check": "blue",
                "loaded_snapshot": 21,
                "compare_snapshot": 22,
                "diff": 1,
            },
            {
                "name": "CDP/LLDP unidirectional",
                "id": "320633253",
                "check": "amber",
                "loaded_snapshot": 10,
                "compare_snapshot": 5,
                "diff": -5,
            },
            {
                "name": "CDP/LLDP unidirectional",
                "id": "320633253",
                "check": "red",
                "loaded_snapshot": 0,
                "compare_snapshot": 100,
                "diff": 100,
            },
        ]

        self.assertEqual(comp, data)
