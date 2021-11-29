import unittest
from unittest.mock import MagicMock, patch

from ipfabric.tools import sites


class UpdateSiteNames(unittest.TestCase):
    def setUp(self) -> None:
        self.usn = sites.UpdateSiteNames(MagicMock(), list())

    def test_post_init_bad_file(self):
        with self.assertRaises(SyntaxError) as err:
            sites.UpdateSiteNames(MagicMock(), 'bad')

    @patch('builtins.open')
    @patch('ipfabric.tools.sites.exists')
    @patch('csv.reader')
    def test_post_init(self, csv, exists, mock_open):
        exists.return_value = True
        csv.return_value = iter([(1, 2), (3, 4)])
        test = sites.UpdateSiteNames(MagicMock(), 'bad')
        self.assertEqual(test.sites, [(1, 2), (3, 4)])

    def test_patch_site(self):
        self.usn.ipf.patch().status_code = 200
        self.assertTrue(self.usn._patch_site('key', 2, 3))

    def test_patch_site_falied(self):
        self.usn.ipf.patch().status_code = 400
        self.assertFalse(self.usn._patch_site('key', 2, 3))

    @patch('ipfabric.tools.sites.UpdateSiteNames._patch_site')
    def test_update_sites(self, patch):
        patch.return_value = True
        self.usn.ipf.inventory.sites.all.return_value = [dict(siteName='old1', siteKey='key', siteUid='uid1'),
                                                         dict(siteName='new2', siteKey='key', siteUid='uid2'),
                                                         dict(siteName='old3', siteKey='key', siteUid='new3')]
        self.usn.sites = [('old1', 'new1'), ('uid2', 'new2'), ('new3', 'new3'), ('bad', 'new4')]
        test = {'updated': [('old1', 'new1'), ('new3', 'new3')], 'errors': [('uid2', 'new2'), ('bad', 'new4')]}
        self.assertEqual(self.usn.update_sites(), test)