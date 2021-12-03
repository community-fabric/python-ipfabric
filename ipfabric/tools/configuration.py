import logging
from collections import defaultdict
from datetime import datetime, timezone
from ipaddress import IPv4Address, AddressValueError
from typing import Any, Union, Optional

from dateutil import parser
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from .helpers import create_regex

logger = logging.getLogger()


class Config(BaseModel):
    config_id: str = Field(alias="_id")
    sn: str
    hostname: str
    config_hash: str = Field(alias="hash")
    status: str
    last_change: datetime = Field(alias="lastChange")
    last_check: datetime = Field(alias="lastCheck")
    text: Optional[str] = None


@dataclass
class DeviceConfigs:
    ipf: Any

    def get_all_configurations(self, device: Optional[str] = None):
        """
        Get all configurations in IP Fabric
        :param device: str: Hostname (case sensitive) filter
        :return: dict: {Hostname: [Config, Config]}
        """
        if device:
            res = self.ipf.fetch_all('tables/management/configuration',
                                     sort={"order": "desc", "column": "lastChange"},
                                     columns=["_id", "sn", "hostname", "lastChange", "lastCheck", "status", "hash"],
                                     filters=dict(hostname=["eq", device]))
            if len(res) == 0:
                logger.warning(f"Could not find any configurations for device '{device}'.")
                return None
        else:
            res = self.ipf.fetch_all('tables/management/configuration',
                                     sort={"order": "desc", "column": "lastChange"},
                                     columns=["_id", "sn", "hostname", "lastChange", "lastCheck", "status", "hash"])
        results = defaultdict(list)
        [results[cfg['hostname']].append(Config(**cfg)) for cfg in res]
        return results

    def _search_ip(self, ip: str, snapshot_id: str = None, log: bool = False) -> dict:
        res = self.ipf.fetch_all('tables/addressing/managed-devs', columns=['ip', 'hostname'],
                                 reports='/technology/addressing/managed-ip',
                                 filters=dict(ip=["eq", ip]))
        if len(res) == 1 and not log:
            return {'hostname': res[0]['hostname']}
        if len(res) == 1 and log:
            res = self.ipf.inventory.devices.all(columns=['hostname', 'taskKey'], snapshot_id=snapshot_id,
                                                 filters=dict(hostname=["eq", res[0]['hostname']]))
            return {'hostname': res[0]['hostname'], 'taskKey': res[0]['taskKey']}
        elif len(res) > 1:
            logger.warning(f"Found multiple entries for IP '{ip}'.")
        elif len(res) == 0:
            logger.warning(f"Could not find a matching IP for '{ip}'.")
        return {'hostname': None}

    def get_configuration(self, device: str, sanitized: bool = True, date: Union[str, tuple] = '$last'):
        """
        Gets last configuration of a device based on hostname or IP
        :param device: str: Hostname or IP
        :param sanitized: bool: Default True to mask passwords
        :param date: Union[str, tuple]: Defaults to latest config. Values in [$last, $prev, $first] or can be a
                                        tuple of a date range to get the latest snapshot in that range.
                                        Date can be string or int in seconds ("11/22/ 1:30", 1637629200)
        :return: Result: Returns a result or None
        """
        if not isinstance(date, tuple) and date not in ["$last", "$prev", "$first"]:
            raise SyntaxError("Date must be in [$last, $prev, $first] or tuple ('startDate', 'endDate')")
        device = self._validate_device(device)['hostname']
        if not device:
            return None
        cfgs = self.get_all_configurations(device)
        if not cfgs:
            return None
        if device:
            cfg = self._get_hash(cfgs[device], date)
            if cfg:
                res = self.ipf.get('/tables/management/configuration/download',
                                   params=dict(hash=cfg.config_hash, sanitized=sanitized))
                res.raise_for_status()
                cfg.text = res.text
                return cfg
            else:
                logger.error(f"Could not find a configuration with date {date}")
        return None

    @staticmethod
    def _get_hash(configs, date):
        if isinstance(date, tuple):
            start, end = date
            start = datetime.fromtimestamp(start, tz=timezone.utc) if isinstance(start, int) else \
                parser.parse(start).replace(tzinfo=timezone.utc)
            end = datetime.fromtimestamp(end, tz=timezone.utc) if isinstance(end, int) else \
                parser.parse(end).replace(tzinfo=timezone.utc)
            for cfg in configs:
                if start < cfg.last_change < end:
                    return cfg
        elif date == '$last':
            return configs[0]
        elif date == '$prev' and len(configs) > 1:
            return configs[1]
        elif date == '$first':
            return configs[-1]
        return None

    def _validate_device(self, device: str, snapshot_id: str = None, log: bool = False) -> dict:
        try:
            if IPv4Address(device):
                return self._search_ip(device, snapshot_id=snapshot_id, log=log)
        except AddressValueError:
            pass
        hostname = create_regex(device)
        res = self.ipf.inventory.devices.all(columns=['hostname', 'taskKey'], filters=dict(hostname=["reg", hostname]),
                                             snapshot_id=snapshot_id)
        if len(res) == 1:
            return {'hostname': res[0]['hostname'], 'taskKey': res[0]['taskKey']}
        elif len(res) == 0:
            logger.warning(f"Could not find a matching device for '{device}' using regex '{hostname}'.")
        elif len(res) > 1:
            logger.warning(f"Found multiple devices matching '{device}' using regex '{hostname}'.")
        return {'hostname': None}

    def get_log(self, device: str, snapshot_id: str = None):
        device = self._validate_device(device, snapshot_id=snapshot_id, log=True)
        if not device['hostname']:
            return None
        res = self.ipf.get('/os/logs/task/' + device['taskKey'])
        res.raise_for_status()
        return res.text
