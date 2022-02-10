from ipfabric import IPFClient
from ipfabric.tools import DeviceConfigs


if __name__ == "__main__":
    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
    cfg = DeviceConfigs(ipf)

    # cfgs = cfg.get_all_configurations()  # Get all Configurations
    #  Returns dictionary like {SN: [Config, Config]} where SN is the IPF Unique Serial Number
    L35AC92_cfgs = cfg.get_all_configurations(device='L35AC92')  # Get all Configurations for device
    #  Returns dictionary like {'a23ffbf': [Config, Config], '91624130': [Config, Config]}
    print(L35AC92_cfgs)
    """
    {
    'a23ffbf': [Config(config_id='61f1f52936add003e73b4848', sn='a23ffbf', hostname='L35AC92', 
        config_hash='daf3d34ceb44870cc7e2647ccb01dd759e2da5b9', status='no change', 
        last_change=datetime.datetime(2022, 1, 27, 1, 28, 9, tzinfo=datetime.timezone.utc), 
        last_check=datetime.datetime(2022, 2, 10, 1, 21, 29, 986000, tzinfo=datetime.timezone.utc), text=None)],
    '91624130': [Config(config_id='5ffdd5f93d1f1b0343af6bd3', sn='91624130', hostname='L35AC92', 
        config_hash='6df7ab1f8dd2eefc757e8719421d81643c2eb6ee', status='no change', 
        last_change=datetime.datetime(2021, 1, 12, 17, 1, 45, tzinfo=datetime.timezone.utc), 
        last_check=datetime.datetime(2021, 4, 6, 23, 3, 15, 77000, tzinfo=datetime.timezone.utc), text=None)]
    }
    """
    print()

    L35AC92_sn_cfgs = cfg.get_all_configurations(sn='a23ffbf')
    #  Returns dictionary like {'a23ffbf': [Config, Config]}
    print(L35AC92_sn_cfgs)
    """
    {
    'a23ffbf': [Config(config_id='61f1f52936add003e73b4848', sn='a23ffbf', hostname='L35AC92', 
        config_hash='daf3d34ceb44870cc7e2647ccb01dd759e2da5b9', status='no change', 
        last_change=datetime.datetime(2022, 1, 27, 1, 28, 9, tzinfo=datetime.timezone.utc), 
        last_check=datetime.datetime(2022, 2, 10, 1, 21, 29, 986000, tzinfo=datetime.timezone.utc), text=None)]
    }
    """
    print()

    L35AC92 = cfg.get_configuration('L35AC92', sanitized=False)  # Display passwords
    print(L35AC92.last_change)
    """
    2021-11-24 00:13:26+00:00
    """
    print()

    L34R3 = cfg.get_configuration('10.35.189.92', date="$prev")  # Method can also accept any managed IP of the device
    # Date can be $last, $prev, $first; $last is default
    print(L34R3.last_change)
    """
    2021-10-18 23:14:27+00:00
    """
    print()

    # Date can also be tuple of start, end which will return the latest config in that time range.
    # If integer timestamp must be seconds not milliseconds.
    L1LB1 = cfg.get_configuration('L1LB1', date=("11/22/2021 1:30", 1637629200))
    print(L1LB1.last_change)
    print(L1LB1.text)
    """
    auth partition Partition1 { }
    auth partition longDescription {
        description "f sf df\" \"dffddfdf"
    }
    ...
    """
    print()

    bad = cfg.get_configuration("bad-device-name")  # Will return None not error.
    print(bad)
    """
    None
    Could not find a matching device for 'bad-device-name' using regex \
        '^[Bb][Aa][Dd]-[Dd][Ee][Vv][Ii][Cc][Ee]-[Nn][Aa][Mm][Ee]$'.
    """
    print()

    log = cfg.get_log('L1LB1', snapshot_id='$last')
    print(log)
    """
    admin15@(L1LB1)(cfg-sync Standalone)(Active)(/Common)(tmos)# show version
    Syntax Error: "version" unexpected argument
    admin15@(L1LB1)(cfg-sync Standalone)(Active)(/Common)(tmos)# uname -a
    Syntax Error: unexpected argument "uname"
    ...
    """
