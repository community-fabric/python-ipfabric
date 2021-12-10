import unittest
from unittest.mock import patch, MagicMock

from httpx import ReadTimeout, HTTPStatusError

from ipfabric.tools import nist


class NIST(unittest.TestCase):
    def test_cve(self):
        cve = nist.CVEs(total_results=1, cves=[], error='None')
        self.assertIsInstance(cve, nist.CVEs)

    def setUp(self) -> None:
        with patch("httpx.Client.__init__", return_value=None) as mock:
            self.vuln = nist.NIST()
        self.cve = dict(totalResults=1, result=dict(CVE_Items=[dict(cve=dict(CVE_data_meta=dict(ID='TEST')))]))


    def test_params(self):
        self.assertEqual(self.vuln.params, {'cpeMatchString': 'cpe:2.3:*:', 'startIndex': 0, 'resultsPerPage': 50})

    @patch('httpx.Client.get')
    def test_check_juniper(self, get):
        get().json.return_value = self.cve
        res = self.vuln.check_cve('juniper', 'junos', '17.2R1.13')
        self.assertIsInstance(res, nist.CVEs)
        self.assertEqual(res.cves, ['TEST'])
        self.assertEqual(res.total_results, 1)
        self.assertIsNone(res.error)

    @patch('httpx.Client.get')
    def test_check_palo(self, get):
        get().json.return_value = self.cve
        res = self.vuln.check_cve('paloalto', 'pan-os', '8.0.5')
        self.assertIsInstance(res, nist.CVEs)

    @patch('httpx.Client.get')
    def test_check_cisco(self, get):
        get().json.return_value = self.cve
        res = self.vuln.check_cve('cisco', 'ios-xe', '15.5(3)S')
        self.assertIsInstance(res, nist.CVEs)

    @patch('httpx.Client.get')
    def test_check_fortinet(self, get):
        get().json.return_value = self.cve
        res = self.vuln.check_cve('fortinet', 'fortigate', '6.0.4,build0231')
        self.assertIsInstance(res, nist.CVEs)

    @patch('httpx.Client.get')
    def test_check_other(self, get):
        get().json.return_value = self.cve
        res = self.vuln.check_cve('riverbed', 'steelhead', '6.5.2a')
        self.assertIsInstance(res, nist.CVEs)

    @patch('httpx.Client.get')
    def test_check_timeout(self, get):
        get().raise_for_status.side_effect = ReadTimeout('Timeout')
        res = self.vuln.check_cve('riverbed', 'steelhead', '6.5.2a')
        self.assertEqual(res.error, 'Timeout')

    @patch('httpx.Client.get')
    def test_check_error(self, get):
        get().raise_for_status.side_effect = HTTPStatusError('Timeout', request=MagicMock(), response=MagicMock())
        res = self.vuln.check_cve('riverbed', 'steelhead', '6.5.2a')
        self.assertEqual(res.error, 'HTTP Error')
