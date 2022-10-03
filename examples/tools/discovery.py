from ipfabric import IPFClient
from ipfabric.tools import DiscoveryHistory


if __name__ == '__main__':
    ipf = IPFClient()
    dh = DiscoveryHistory(ipf)

    # Default sorting is always timestamp descending

    print(dh.get_all_history(ts_format='utc')[0])  # Default
    """
    {'id': '1109519883', 'sn': 'a4dff08', 'hostname': 'L77R8-LEAF2.ipf.ipfabric.io', 'loginIp': '10.77.10.8', 
    'loginType': 'ssh', 'ts': '2022-09-29T14:40:29+00:00', 'username': 'admin15', 'usernameNotes': None}
    """

    print(dh.get_all_history(ts_format='datetime')[0])
    """
    {'id': '1109519883', 'sn': 'a4dff08', 'hostname': 'L77R8-LEAF2.ipf.ipfabric.io', 'loginIp': '10.77.10.8', 
    'loginType': 'ssh', 'ts': datetime.datetime(2022, 9, 29, 14, 40, 29, tzinfo=datetime.timezone.utc), 
    'username': 'admin15', 'usernameNotes': None}
    """

    print(dh.get_all_history(ts_format='int')[0])  # Note timestamp is in milliseconds not seconds
    """
    {'id': '1109519883', 'sn': 'a4dff08', 'hostname': 'L77R8-LEAF2.ipf.ipfabric.io', 'loginIp': '10.77.10.8', 
    'loginType': 'ssh', 'ts': 1664462429803, 'username': 'admin15', 'usernameNotes': None}
    """

    print(dh.get_history_date('2022-09-28')[0])  # Can also specify timestamp as an integer (must be seconds)
    # This will return all history from that date to now
    """
    {'id': '1109519883', 'sn': 'a4dff08', 'hostname': 'L77R8-LEAF2.ipf.ipfabric.io', 'loginIp': '10.77.10.8', 
    'loginType': 'ssh', 'ts': '2022-09-29T14:40:29+00:00', 'username': 'admin15', 'usernameNotes': None}
    """

    print(dh.get_history_date(('2022-09-01', '2022-09-27'))[0])  # Can also specify timestamp as an integer
    """
    {'id': '1149496501', 'sn': '5000.0013.0000/vGw-1', 'hostname': 'L71-VSX1/vGw-1', 'loginIp': '10.71.117.121', 
    'loginType': 'ssh', 'ts': '2022-09-22T20:23:53+00:00', 'username': 'admin15', 'usernameNotes': None}
    """

    snap_history, snap_no_history = dh.get_snapshot_history(snapshot_id='$last')
    print(snap_history[0])
    """
    {'id': '1109020999', 'sn': 'a2dff68', 'hostname': 'L45R4', 'loginIp': '10.45.114.104', 'loginType': 'ssh', 
    'ts': '2022-09-22T20:23:36+00:00', 'username': 'admin15', 'usernameNotes': None}
    """
    print(snap_no_history[0])  # Usually will be Access Points or devices discovered via API
    """
    {'sn': 'D76E5C23EEC32A2E', 'hostname': 'Branch-A', 'loginIp': None, 'loginType': 'api'}
    """

    deleted = dh.delete_history_prior_to_ts('2022-08-05')  # Can also specify timestamp as an integer (must be seconds)
    print(deleted[0])
    """
    {'id': '1109088301', 'sn': '5000.00ba.c6f8', 'hostname': 'L33R8', 'loginIp': '10.33.255.108', 'loginType': 'ssh', 
    'ts': '2022-08-04T19:23:54+00:00', 'username': 'admin15', 'usernameNotes': None}
    """
