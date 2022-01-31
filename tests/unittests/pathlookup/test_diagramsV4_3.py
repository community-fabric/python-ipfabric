import unittest
from unittest.mock import MagicMock, patch

import ipfabric.pathlookup
from ipfabric.pathlookup import DiagramV43


class Models(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = DiagramV43(MagicMock())

    @patch('ipfabric.pathlookup.graphs.IPFPath.check_subnets')
    @patch('ipfabric.pathlookup.diagramsV4_3.DiagramV43.check_proto')
    @patch('ipfabric.pathlookup.graphs.IPFPath._query')
    def test_unicast(self, query, proto, subnets):
        query.return_value = True
        self.assertTrue(self.graph.unicast('ip', 'ip', overlay=dict(test=1)))

    @patch('ipfabric.pathlookup.graphs.IPFPath.check_subnets')
    @patch('ipfabric.pathlookup.diagramsV4_3.DiagramV43.check_proto')
    @patch('ipfabric.pathlookup.graphs.IPFPath._query')
    def test_multicast(self, query, proto, subnets):
        subnets.return_value = False
        query.return_value = True
        self.assertTrue(self.graph.multicast('ip', 'ip', rec_ip='ip', overlay=dict(test=1)))

    @patch('ipfabric.pathlookup.diagramsV4_3.DiagramV43.check_proto')
    def test_multicast_failed(self, proto):
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0/24', '10.0.0.1')
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0', '10.0.0.1', rec_ip='10.0.0.0/24')

    def test_check_proto_failed(self):
        with self.assertRaises(SyntaxError) as err:
            self.graph.check_proto(dict(protocol='tcp'), flags=['bad'], icmp=None)

    def test_check_proto_flags(self):
        params = self.graph.check_proto(dict(protocol='tcp', l4Options=dict()), flags=['syn'], icmp=None)
        self.assertEqual(params, {'protocol': 'tcp', 'l4Options': {'flags': ['syn']}})

    def test_check_proto_icmp(self):
        params = dict(
            protocol='icmp',
            l4Options=dict(
                srcPorts=3,
                dstPorts=4
            )
        )
        params = self.graph.check_proto(params, flags=['syn'], icmp=ipfabric.pathlookup.ECHO_REPLY)
        self.assertEqual(params, {'protocol': 'icmp', 'l4Options': {'code': 0, 'type': 0}})

    def test_check_proto_icmp_failed(self):
        params = dict(protocol='icmp')
        with self.assertRaises(SyntaxError) as err:
            self.graph.check_proto(params, flags=None, icmp=None)
