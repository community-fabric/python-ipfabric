from datetime import datetime, timezone
from typing import Union

from dateutil import parser


def convert_timestamp(ts: int, to_utc: bool = False):
    dt = datetime.fromtimestamp(int(ts / 1000), tz=timezone.utc)
    return dt.isoformat() if to_utc else dt


def date_parser(timestamp: Union[int, str]):
    return (
        datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if isinstance(timestamp, int)
        else parser.parse(timestamp).replace(tzinfo=timezone.utc)
    )
