"""
Just some helper functions that make IP Fabric more usable.
"""

from pytz import timezone

from ipfabric.tools.shared import convert_timestamp, parse_mac

if __name__ == '__main__':
    dt = convert_timestamp(1647734412345)
    print({dt})
    """{datetime.datetime(2022, 3, 20, 0, 0, 12, 345000, tzinfo=datetime.timezone.utc)}"""
    print(convert_timestamp(1647734412345, ts_format='iso'))
    """2022-03-20T00:00:12.345+00:00"""
    print(convert_timestamp(1647734412345, ts_format='iso', milliseconds=False))
    """2022-03-20T00:00:12+00:00"""
    print(convert_timestamp(1647734412345, ts_format='ziso'))
    """2022-03-20T00:00:12.345Z"""
    print(convert_timestamp(1647734412345, ts_format='date'))
    """2022-03-20"""
    print(convert_timestamp(1647734412345, ts_format='iso', tzinfo=timezone('America/New_York')))
    """2022-03-19T20:00:12.345-04:00"""

    print(parse_mac('01-23-45-67-89-ab'))
    """0123.4567.89ab"""
    print(parse_mac('0021.A4AE.C49b'))
    """0021.a4ae.c49b"""
    print(parse_mac('002184789d11'))
    """0021.8478.9d11"""
    print(parse_mac('00:1f:ca:08:b6:10'))
    """001f.ca08.b610"""
    print(parse_mac('BADMAC'))
    """
    None
    BADMAC is not a valid mac.
    """


