import unittest
from unittest.mock import MagicMock, patch

from ipfabric.pathlookup import Diagram


class Models(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Diagram(MagicMock())

    @patch('ipfabric.pathlookup.graphs.IPFPath.check_subnets')
    @patch('ipfabric.pathlookup.diagrams.Diagram.check_proto')
    @patch('ipfabric.pathlookup.graphs.IPFPath._query')
    def test_unicast(self, query, proto, subnets):
        query.return_value = True
        self.assertTrue(self.graph.unicast('ip', 'ip', overlay=dict(test=1)))

    @patch('ipfabric.pathlookup.graphs.IPFPath.check_subnets')
    @patch('ipfabric.pathlookup.diagrams.Diagram.check_proto')
    @patch('ipfabric.pathlookup.graphs.IPFPath._query')
    def test_multicast(self, query, proto, subnets):
        subnets.return_value = False
        query.return_value = True
        self.assertTrue(self.graph.multicast('ip', 'ip', rec_ip='ip', overlay=dict(test=1)))

    @patch('ipfabric.pathlookup.diagrams.Diagram.check_proto')
    def test_multicast_failed(self, proto):
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0/24', '10.0.0.1')
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0', '10.0.0.1', rec_ip='10.0.0.0/24')

    def test_check_proto_failed(self):
        with self.assertRaises(SyntaxError) as err:
            self.graph.check_proto(dict(protocol='tcp'), flags=['bad'])

    def test_check_proto_flags(self):
        params = self.graph.check_proto(dict(protocol='tcp'), flags=['syn'])
        self.assertEqual(params, {'protocol': 'tcp', 'flags': ['syn']})

    def test_check_proto_icmp(self):
        params = dict(
            protocol='icmp',
            startingPort=1,
            destinationPort=2,
            sourcePort=3,
            groupPort=4
        )
        params = self.graph.check_proto(params, flags=['syn'])
        self.assertEqual(params, {'protocol': 'icmp'})
