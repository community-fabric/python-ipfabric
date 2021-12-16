from ipfabric import IPFClient
from ipfabric.tools import UpdateSiteNames


if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)

    upd = UpdateSiteNames(ipf, 'site_updates.csv', dry_run=True)  # CSV file: oldSiteName, newSiteName
    res = upd.update_sites()
    print(res)
    """
    {'updated': [('MPLS', 'MPLS-NEW')], 'errors': []}
    """

    upd.dry_run = False
    res = upd.update_sites()
    print(res)
    """
    Changed MPLS to MPLS-NEW
    {'updated': [('MPLS', 'MPLS-NEW')], 'errors': []}
    """

    upd = UpdateSiteNames(ipf, [('MPLS-NEW', 'MPLS')])  # List of Tuples: [(oldSiteName, newSiteName)]
    res = upd.update_sites()
    print(res)
    """
    Changed MPLS-NEW to MPLS
    {'updated': [('MPLS-NEW', 'MPLS')], 'errors': []}
    """