from httpx import Client, ReadTimeout, HTTPStatusError
from pydantic import BaseModel, Field


class CVEs(BaseModel):
    total_results: int
    cves: list
    error: str = Field(default=None)


class NIST(Client):
    def __init__(self, timeout, cve_limit):
        super().__init__(base_url='https://services.nvd.nist.gov/rest/json/cves/1.0', timeout=timeout)
        self.cve_limit = cve_limit

    @property
    def params(self):
        return {
            'cpeMatchString': 'cpe:2.3:*:',
            'startIndex': 0,
            'resultsPerPage': self.cve_limit
        }

    def check_cve(self, vendor: str, family: str, version: str):
        """

        :param vendor: str: Vendor for the device to be checked
        :param family: str: Family of the device to be checked
        :param version: str: Software version of the device to be checked
        :return:
        """
        params = self.params
        if vendor == 'juniper':
            params['cpeMatchString'] += vendor + ":" + family + ":" + version[:version.rfind('R') + 2].replace('R', ':r')
        elif vendor == 'paloalto':
            params['cpeMatchString'] += 'palo_alto' + ":" + family + ":" + version
        elif vendor == 'cisco':
            params['cpeMatchString'] += 'cisco:' + family + ':' + (version.replace('(', '.')).replace(')', '.')
        elif vendor == 'fortinet' and family == 'fortigate':
            params['cpeMatchString'] += 'fortinet:fortios:' + version.replace(',', '.')
        else:
            v = str(version).split(',')[0]
            params['cpeMatchString'] += str(vendor) + ":" + str(family) + ":" + v

        try:
            res = self.get('', params=params)
            res.raise_for_status()
            data = res.json()
            cves = CVEs(total_results=data['totalResults'],
                        cves=[i['cve']['CVE_data_meta']['ID'] for i in data['result']['CVE_Items']])
            return cves
        except ReadTimeout:
            return CVEs(total_results=0, cves=[], error='Timeout')
        except HTTPStatusError:
            return CVEs(total_results=0, cves=[], error='HTTP Error')
