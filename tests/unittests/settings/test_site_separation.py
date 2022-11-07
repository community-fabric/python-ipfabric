import unittest
from unittest.mock import MagicMock

from ipfabric.settings.site_separation import SiteSeparation


class TestSiteSeparation(unittest.TestCase):
    def setUp(self) -> None:
        self.site = SiteSeparation(MagicMock())

    def test_get_separation_rules(self):
        self.site.ipf.get().json.return_value = [1]
        self.assertEqual(self.site.get_separation_rules()[0], 1)

    def test_get_snmp_matches(self):
        self.site.ipf.post().json.return_value = [1]
        self.assertEqual(self.site.get_snmp_matches('.*(LAB01)', 'uppercase')[0], 1)

    def test_get_hostname_matches(self):
        self.site.ipf.post().json.return_value = [1]
        self.assertEqual(self.site.get_hostname_matches('.*(LAB01)', 'uppercase')[0], 1)

    def test_create_rule_fail(self):
        with self.assertRaises(SyntaxError) as err:
            self.site._create_rule('bad', 'test')

    def test_get_rule_matches(self):
        rule = {
            "type": "regexSnmpLocation",
            "id": "910adccc-c98f-4778-aab7-da644539ca69",
            "note": "LAB1",
            "regex": ".*(LAB01)",
            "siteName": None,
            "transformation": "uppercase"
        }
        self.site.ipf.post().json.return_value = [1]
        self.assertEqual(self.site.get_rule_matches(rule)[0], 1)