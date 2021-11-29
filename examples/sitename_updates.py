from ipfabric import IPFClient
from ipfabric.tools import UpdateSiteNames


if __name__ == "__main__":
    ipf = IPFClient('https://demo3.ipfabric.io')

    upd = UpdateSiteNames(ipf, 'site_updates.csv', dry_run=True)  # CSV file: oldSiteName, newSiteName
    res = upd.update_sites()
    print(res)
    """
    {'updated': [('MPLS', 'MPLS-NEW')], 'errors': []}
    """

    upd = UpdateSiteNames(ipf, 'site_updates.csv')  # CSV file: oldSiteName, newSiteName
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