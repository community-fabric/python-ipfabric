import unittest
from unittest.mock import MagicMock

from ipfabric.tools.builtin_checks import NonRedundantLinks, SinglePointsFailure


class Checks(unittest.TestCase):
    def setUp(self) -> None:
        self.ipf = MagicMock()
        self.ipf.inventory.sites.all.return_value = [{"siteName": "Test"}]
        self.ipf.graphs.site.return_value = {
            "graphResult": {
                "graphData": {
                    "edges": {
                        "39380579": {
                            "source": "69240849",
                            "target": "9A0MD0N6T4F",
                            "intentCheckResult": 30,
                            "labels": {
                                "source": [{"type": "intName", "text": "Et0/0"}],
                                "target": [{"type": "intName", "text": "GigabitEthernet0/1"}],
                            },
                        },
                        "39380580": {
                            "source": "SOURCE",
                            "target": "TARGET",
                            "intentCheckResult": 0,
                            "labels": {
                                "source": [{"type": "intName", "text": "Et0/0"}],
                                "target": [{"type": "intName", "text": "GigabitEthernet0/1"}],
                            },
                        },
                    },
                    "nodes": {
                        "69240849": {
                            "id": "69240849",
                            "label": "L1R13",
                            "type": "router",
                            "intentCheckResult": 30,
                        },
                        "9A0MD0N6T4F": {"id": "9A0MD0N6T4F", "label": "L1FW1", "type": "fw"},
                    },
                }
            }
        }

    def test_single_points(self):
        spf = SinglePointsFailure(self.ipf)
        devices = spf.list()
        self.assertEqual(devices[0], {"device": "L1R13", "type": "router"})

    def test_non_redundant_links(self):
        nrl = NonRedundantLinks(self.ipf)
        links = nrl.list()
        self.assertEqual(
            links[0], {"source": "L1R13", "source_int": "Et0/0", "target": "L1FW1", "target_int": "GigabitEthernet0/1"}
        )
