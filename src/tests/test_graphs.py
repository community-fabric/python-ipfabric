import ipaddress
import unittest
from ipfabric.graphs import IPFPath
from unittest.mock import MagicMock, patch


class Models(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = IPFPath(MagicMock())

    def test_style(self):
        self.graph.style = 'png'
        self.assertEqual(self.graph.style, 'png')

    def test_invalid_style(self):
        with self.assertRaises(ValueError) as err:
            self.graph.style = 'bad'

    def test_query(self):
        self.graph.client.post().json.return_value = dict(test="hello")
        self.graph.client.post().content = b'Hello'
        self.assertEqual(self.graph._query({}), dict(test="hello"))
        self.graph.style = 'png'
        self.assertEqual(self.graph._query({}), b'Hello')
        self.graph.style = 'svg'
        self.assertEqual(self.graph._query({}), b'Hello')

    @patch('ipfabric.graphs.IPFPath.check_subnets')
    @patch('ipfabric.graphs.IPFPath.check_proto')
    @patch('ipfabric.graphs.IPFPath._query')
    def test_unicast(self, query, proto, subnets):
        query.return_value = True
        self.assertTrue(self.graph.unicast('ip', 'ip'))

    @patch('ipfabric.graphs.IPFPath.check_subnets')
    @patch('ipfabric.graphs.IPFPath.check_proto')
    @patch('ipfabric.graphs.IPFPath._query')
    def test_multicast(self, query, proto, subnets):
        subnets.return_value = False
        query.return_value = True
        self.assertTrue(self.graph.multicast('ip', 'ip', rec_ip='ip'))

    @patch('ipfabric.graphs.IPFPath.check_proto')
    def test_multicast_failed(self, proto):
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0/24', '10.0.0.1')
        with self.assertRaises(SyntaxError) as err:
            self.graph.multicast('10.0.0.0', '10.0.0.1', rec_ip='10.0.0.0/24')

    @patch('ipfabric.graphs.IPFPath.check_subnets')
    @patch('ipfabric.graphs.IPFPath._query')
    def test_host_to_gw(self, query, subnets):
        query.return_value = True
        self.assertTrue(self.graph.host_to_gw('ip'))

    def test_check_subnets(self):
        self.assertTrue(self.graph.check_subnets('10.0.0.0/24'))
        self.assertFalse(self.graph.check_subnets('10.0.0.1'))

    def test_check_subnets_failed(self):
        with self.assertRaises(ipaddress.AddressValueError) as err:
            self.graph.check_subnets('bad ip')

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
