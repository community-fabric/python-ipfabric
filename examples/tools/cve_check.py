from pprint import pprint

from ipfabric import IPFClient
from ipfabric.tools import Vulnerabilities

if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    vuln = Vulnerabilities(ipf)

    device = vuln.check_device('L47R6')
    pprint(device)
    """
    [Version(vendor='cisco', family='ios', version='15.2(4)M1', cves=CVEs(total_results=28, 
    cves=['CVE-2021-34703', 'CVE-2021-1460', ...], error=None), hostname='L47R6', site='L47')]
    """
    print()

    site = vuln.check_site('L47')
    pprint(f"Number of devices: {len(site)}")
    pprint(site[0])
    """
    Number of devices: 21
    Version(vendor='cisco', family='ios', version='15.2(20170809:194209)',
    cves=CVEs(total_results=0, cves=[], error=None), hostname='L47AC14', site='L47')
    """
    print()

    vendor = vuln.check_versions('cisco')
    pprint(f"Number of versions: {len(vendor)}")
    pprint([v.version for v in vendor])
    """
    19
    ['9.1(7)16',
     '6.4.0 (Build 102)',
     '12.4(15)T17',
     '15.4(2)T',
     '15.4(2)T4',
     '15.5(2)T',
    ...]
    """
    print()

    cves = vuln.check_versions()  # Check all software versions.
    print("Total effected software versions:")
    pprint(len([v for v in cves if v.cves.total_results > 0]))
    print("Total errors:")
    pprint(len([v for v in cves if v.cves.error]))
    """
    Total effected software versions:
    27
    Total errors:
    1
    """

