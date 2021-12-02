import unittest
from unittest.mock import patch, MagicMock

from ipfabric.tools import vulnerabilities
from ipfabric.tools.nist import CVEs


class Version(unittest.TestCase):
    def test_version(self):
        version = vulnerabilities.Version(vendor='Cisco', family='ios', version='1', hostname='TEST', site='TEST',
                                          cves=CVEs(total_results=1, cves=[], error='None'))
        self.assertIsInstance(version, vulnerabilities.Version)


class Vulnerabilities(unittest.TestCase):
    def setUp(self) -> None:
        with patch('ipfabric.tools.vulnerabilities.NIST') as mock:
            self.vuln = vulnerabilities.Vulnerabilities(MagicMock())
        self.vuln.nist.check_cve.return_value = CVEs(total_results=1, cves=[], error='None')

    def test_check_versions_cve(self):
        res = self.vuln._check_versions([dict(version='1', vendor='cisco', family='ios', hostname='TEST',
                                              siteName='TEST')])
        self.assertIsInstance(res[0], vulnerabilities.Version)
        self.assertIsInstance(res[0].cves, CVEs)

    @patch('ipfabric.tools.vulnerabilities.Vulnerabilities._check_versions')
    def test_check_versions(self, versions):
        versions.return_value = [vulnerabilities.Version(version='1', vendor='cisco', family='ios', hostname='TEST',
                                                         site='TEST', cves=CVEs(total_results=1, cves=['TEST']))]
        self.vuln.ipf.inventory.devices.all.return_value = [dict(version='1', vendor='cisco', family='ios')]
        cve = self.vuln.check_versions()
        self.assertIsInstance(cve[0], vulnerabilities.Version)
        self.assertIsInstance(cve[0].cves, CVEs)

    @patch('ipfabric.tools.vulnerabilities.Vulnerabilities._check_versions')
    def test_check_device(self, versions):
        versions.return_value = [vulnerabilities.Version(version='1', vendor='cisco', family='ios', hostname='TEST',
                                                         site='TEST', cves=CVEs(total_results=1, cves=['TEST']))]
        self.vuln.ipf.inventory.devices.all.return_value = [dict(version='1', vendor='cisco', family='ios')]
        cve = self.vuln.check_device('TEST')
        self.assertIsInstance(cve[0], vulnerabilities.Version)
        self.assertIsInstance(cve[0].cves, CVEs)

    @patch('ipfabric.tools.vulnerabilities.Vulnerabilities._check_versions')
    def test_check_site(self, versions):
        versions.return_value = [vulnerabilities.Version(version='1', vendor='cisco', family='ios', hostname='TEST',
                                                         site='TEST', cves=CVEs(total_results=1, cves=['TEST']))]
        self.vuln.ipf.inventory.devices.all.return_value = [dict(version='1', vendor='cisco', family='ios')]
        cve = self.vuln.check_site('TEST')
        self.assertIsInstance(cve[0], vulnerabilities.Version)
        self.assertIsInstance(cve[0].cves, CVEs)

    def test_delete(self):
        self.vuln.nist.close.side_effect = AttributeError()
        del self.vuln
        self.assertTrue(True)
