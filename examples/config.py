from ipfabric import IPFClient
from ipfabric.tools import Configurations


if __name__ == "__main__":
    ipf = IPFClient('https://demo3.ipfabric.io', '07317f03dcfa56d978ede33f140262aa')
    cfg = Configurations(ipf)

    L34R3 = cfg.get_configuration('L34R3', sanitized=False)  # Display passwords
    print(L34R3.timestamp)
    """
    2021-11-24 00:13:26+00:00
    """
    print()

    L34R3 = cfg.get_configuration('L34R3', date="$prev")  # Date can be $last, $prev, $first; $last is default
    print(L34R3.timestamp)
    """
    2021-10-18 23:14:27+00:00
    """
    print()

    # Date can also be tuple of start, end which will return the latest config in that time range.
    # If integer timestamp must be seconds not milliseconds.
    L1LB1 = cfg.get_configuration('L1LB1', date=("11/22/2021 1:30", 1637629200))
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
    Device bad-device-name not found in Configurations
    """

