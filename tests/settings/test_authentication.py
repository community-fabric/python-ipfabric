import datetime
import ipaddress
import unittest
from unittest.mock import MagicMock, patch
from ipfabric.settings import authentication


class Models(unittest.TestCase):
    def test_expiration(self):
        self.assertEqual(authentication.Expiration(enabled=False), dict(enabled=False, value=None))

    def test_credential(self):
        cred = authentication.Credential(network=['10.0.0.0/24'], excludeNetworks=[],
                                         expirationDate=dict(enabled=False), id='ID', password='PASS', username='USER',
                                         priority=1, syslog=False)
        self.assertIsInstance(cred, authentication.Credential)

    def test_privilege(self):
        cred = authentication.Privilege(includeNetworks=['10.0.0.0/24'], excludeNetworks=[],
                                        expirationDate=dict(enabled=False), id='ID', password='PASS', username='USER',
                                        priority=1)
        self.assertIsInstance(cred, authentication.Privilege)


class Authentication(unittest.TestCase):
    def setUp(self) -> None:
        self.cred = {
            "excludeNetworks": [],
            "expirationDate": {
                "enabled": False
            },
            "id": "918d1a0f-98b1-4895-ba51-340f7f2cf6cd",
            "password": "829ec229e38314",
            "priority": 1,
            "syslog": True,
            "username": "admin15",
            "network": [
                "0.0.0.0/0"
            ]
        }
        self.priv = {
            "excludeNetworks": [],
            "expirationDate": {
                "enabled": False
            },
            "id": "0a5b528d-4fd1-4e62-91e7-e565affa058f",
            "includeNetworks": [
                "0.0.0.0/0"
            ],
            "password": "829ec229e38314",
            "username": "admin15",
            "priority": 1
        }
        self.data = {
            "network": [
                "0.0.0.0/0"
            ],
            "excludeNetworks": [],
            "syslog": False,
            "expirationDate": {
                "enabled": True,
                "value": "2021-11-24 23:59:59"
            },
            "password": "test",
            "username": "test"
        }
        self.auth = authentication.Authentication(client=MagicMock())
        self.auth.credentials = {1: authentication.Credential(**self.cred)}
        self.auth.enables = {1: authentication.Privilege(**self.priv)}

    def test_credentials(self):
        self.auth.client.get().json.return_value = dict(data=[self.cred])
        self.assertIsInstance(self.auth.credentials[1], authentication.Credential)

    def test_enables(self):
        self.auth.client.get().json.return_value = dict(data=[self.priv])
        self.assertIsInstance(self.auth.enables[1], authentication.Privilege)

    def test_create_credential(self):
        self.auth.client.post().json.return_value = self.cred
        cred = self.auth.create_credential('test', 'password')
        self.assertIsInstance(cred, authentication.Credential)

    def test_create_enable(self):
        self.auth.client.post().json.return_value = self.priv
        priv = self.auth.create_enable('test', 'password')
        self.assertIsInstance(priv, authentication.Privilege)

    def test_create_payload_failed(self):
        with self.assertRaises(ipaddress.AddressValueError) as err:
            self.auth._create_payload('test', 'pass', None, None, ['hello world'], False)

    def test_create_payload_expires(self):
        payload = self.auth._create_payload('test', 'pass', None, None, None, '11-23-2021T23:59:59')
        self.assertEqual(payload["expirationDate"]["value"], '2021-11-23 23:59:59')

    @patch('ipfabric.settings.authentication.Authentication.get_credentials')
    def test_delete_cred(self, mock_call):
        self.assertIsNone(self.auth.delete_credential('TEST'))

    @patch('ipfabric.settings.authentication.Authentication.get_enables')
    def test_delete_enable(self, mock_call):
        self.assertIsNone(self.auth.delete_enable('TEST'))

    @patch('ipfabric.settings.authentication.Authentication.get_credentials')
    def test_update_cred(self, mock_call):
        creds = self.auth.update_cred_priority(self.auth.credentials)
        self.assertEqual(creds, self.auth.credentials)

    @patch('ipfabric.settings.authentication.Authentication.get_enables')
    def test_update_enable(self, mock_call):
        priv = self.auth.update_enable_priority(self.auth.enables)
        self.assertEqual(priv, self.auth.enables)
