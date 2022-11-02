import unittest
from unittest.mock import MagicMock, patch

from ipfabric.settings.attributes import Attributes


class TestAttributes(unittest.TestCase):
    def setUp(self) -> None:
        self.ipf_attr = Attributes(MagicMock(), snapshot_id=None)

    def test_local_attributes(self):
        ipf = MagicMock()
        snapshot = MagicMock()
        snapshot.snapshot_id = 'TEST'
        ipf.get_snapshot.return_value = snapshot
        ipf_attr = Attributes(ipf, snapshot_id='$last')
        self.assertEqual(ipf_attr.snapshot_id, 'TEST')

    def test_check_attribute_name_fail(self):
        with self.assertRaises(NameError) as err:
            self.ipf_attr.check_attribute_name({'_BAD-NAME'})

    def test_update_local_attr_from_global_fail(self):
        with self.assertRaises(ImportError) as err:
            self.ipf_attr.update_local_attr_from_global()

    def test_all(self):
        self.ipf_attr.client.fetch_all.return_value = [{'id': '9786859055',
                                                        'name': 'siteName',
                                                        'sn': 'a23ffc0',
                                                        'value': '35HEADOFFICE'}]
        self.assertEqual(self.ipf_attr.all()[0]['id'], '9786859055')

    def test_set_attribute_by_sn(self):
        self.ipf_attr.client.post().json.return_value = {'id': '9786859055',
                                                        'name': 'siteName',
                                                        'sn': 'a23ffc0',
                                                        'value': '35HEADOFFICE'}
        self.assertEqual(self.ipf_attr.set_attribute_by_sn('a23ffc0', 'siteName', '35HEADOFFICE')['id'], '9786859055')

    def test_set_attributes_by_sn(self):
        self.ipf_attr.client.put().json.return_value = [{'id': '9786859055',
                                                         'name': 'siteName',
                                                         'sn': 'a23ffc0',
                                                         'value': '35HEADOFFICE'}]
        a = [{'name': 'siteName', 'sn': 'a23ffc0', 'value': '35HEADOFFICE'}]
        self.assertEqual(self.ipf_attr.set_attributes_by_sn(a)[0]['id'], '9786859055')

    def test_set_site_by_sn(self):
        self.ipf_attr.client.post().json.return_value = {'id': '9786859055',
                                                         'name': 'siteName',
                                                         'sn': 'a23ffc0',
                                                         'value': '35HEADOFFICE'}
        self.assertEqual(self.ipf_attr.set_site_by_sn('a23ffc0', '35HEADOFFICE')['id'], '9786859055')

    def test_set_sites_by_sn(self):
        self.ipf_attr.client.put().json.return_value = [{'id': '9786859055',
                                                         'name': 'siteName',
                                                         'sn': 'a23ffc0',
                                                         'value': '35HEADOFFICE'}]
        a = [{'name': 'siteName', 'sn': 'a23ffc0'}]
        self.assertEqual(self.ipf_attr.set_sites_by_sn(a)[0]['id'], '9786859055')

    def test_delete_attribute_by_sn(self):
        self.ipf_attr.client.request.return_value = MagicMock()
        self.assertTrue(self.ipf_attr.delete_attribute_by_sn('9786859055'))

    def test_delete_attribute(self):
        self.ipf_attr.client.request.return_value = MagicMock()
        self.assertTrue(self.ipf_attr.delete_attribute({'id': '9786859055'}))

    @patch('ipfabric.settings.attributes.Attributes.all')
    def test_update_local_attr_from_global(self, all):
        ipf = MagicMock()
        snapshot = MagicMock()
        snapshot.snapshot_id = 'TEST'
        ipf.get_snapshot.return_value = snapshot
        ipf_attr = Attributes(ipf, snapshot_id='$last')
        ipf_attr.client.fetch_all.return_value = [{'id': '9786859055',
                                                        'name': 'siteName',
                                                        'sn': 'a23ffc0',
                                                        'value': '35HEADOFFICE'}]
        all.return_value = [{'id': '9786859055',
                             'name': 'siteName',
                             'sn': 'a23ffc0',
                             'value': '35HEADOFFICE'}]
        ipf_attr.client.request.return_value = MagicMock()
        ipf_attr.client.put().json.return_value = [{'id': '9786859055',
                                                         'name': 'siteName',
                                                         'sn': 'a23ffc0',
                                                         'value': '35HEADOFFICE'}]
        self.assertTrue(ipf_attr.update_local_attr_from_global())
