import logging
from datetime import datetime, timezone
from typing import Union

import macaddress
from dateutil import parser
from pytz import BaseTzInfo, utc

logger = logging.getLogger("python-ipfabric")


class MAC(macaddress.MAC):
    formats = ("xxxx.xxxx.xxxx",) + macaddress.MAC.formats


def convert_timestamp(ts: int, ts_format: str = "datetime", milliseconds: bool = True, tzinfo: BaseTzInfo = utc):
    """
    Converts IP Fabric timestamp in milliseconds to a formatted time
    :param ts: int: Timestamp in milliseconds (IP Fabric's returned format)
    :param ts_format: str: Default datetime, can be ['datetime', 'iso', 'ziso', 'date']
    :param milliseconds: bool: Default True to return milliseconds, False returns seconds
    :param: tzinfo: pytz object: Default utc
    :return:
    """
    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone(tzinfo)
    if ts_format == "datetime":
        return dt
    elif ts_format == "iso":
        return dt.isoformat(timespec="milliseconds" if milliseconds else "seconds")
    elif ts_format == "ziso":
        return dt.isoformat(timespec="milliseconds" if milliseconds else "seconds").replace("+00:00", "Z")
    elif ts_format == "date":
        return dt.date()
    else:
        raise SyntaxError(f"{ts_format} is not one of ['datetime', 'iso', 'ziso', 'date'].")


def date_parser(timestamp: Union[int, str]):
    return (
        datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if isinstance(timestamp, int)
        else parser.parse(timestamp).replace(tzinfo=timezone.utc)
    )


def parse_mac(mac_address):
    """
    Takes any format MAC address and return IP Fabric format.
    :param mac_address: Union[str, list]: String or list of MAC address
    :return: Union[str, list]: String or list of MAC address
    """

    def mac_format(mac):
        try:
            return str(MAC(mac.strip())).lower()
        except ValueError:
            logger.warning(f"{mac.strip()} is not a valid mac.")
            return None

    if isinstance(mac_address, str):
        return mac_format(mac_address)
    elif isinstance(mac_address, list):
        parsed = list()
        for m in mac_address:
            if not m:
                continue
            mac = mac_format(m)
            if mac:
                parsed.append(mac)

        return parsed
    return None
