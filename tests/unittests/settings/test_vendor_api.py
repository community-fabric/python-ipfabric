import unittest
from unittest.mock import MagicMock

from ipfabric.settings import VendorAPI, AWS


class TestVendorAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.api = VendorAPI(client=MagicMock())

    def test_get_vendor_apis(self):
        self.api.client.get().json.return_value = [{'id': '1'}]
        self.assertEqual(self.api.get_vendor_apis()[0]['id'], '1')

    def test_add_vendor_api(self):
        self.api.client.post().json.return_value = [{'id': '1'}]
        aws = AWS(apiKey='TEST', apiSecret='TEST', regions=['eu-central-1'], assumeRoles=['test'])
        self.assertEqual(self.api.add_vendor_api(aws)[0]['id'], '1')
        aws = AWS(apiKey='TEST', apiSecret='TEST', regions=['eu-central-1'])
        self.assertEqual(self.api.add_vendor_api(aws)[0]['id'], '1')

    def test_delete_vendor_api(self):
        self.api.client.delete().status_code = 204
        self.assertEqual(self.api.delete_vendor_api({'id': '1'}), 204)
        self.assertEqual(self.api.delete_vendor_api(1), 204)

    def test_aws_bad_region(self):
        with self.assertRaises(ValueError) as err:
            AWS(apiKey='TEST', apiSecret='TEST', regions=['bad-region'])
