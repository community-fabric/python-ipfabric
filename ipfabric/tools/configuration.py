import logging
from collections import defaultdict
from datetime import datetime, timezone
from ipaddress import IPv4Address, AddressValueError
from typing import Any, Union

from dateutil import parser
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

logger = logging.getLogger()


class Config(BaseModel):
    config_id: str = Field(alias="_id")
    sn: str
    hostname: str
    config_hash: str = Field(alias="hash")
    status: str
    last_change: datetime = Field(alias="lastChange")
    last_check: datetime = Field(alias="lastCheck")


class Result(BaseModel):
    timestamp: datetime
    text: str


@dataclass
class DeviceConfigs:
    client: Any
    managed_ip: dict = Field(default=dict())
    configs: dict = Field(default=dict())

    def __post_init__(self):
        self._get_managed_ips()
        self._get_all_configurations()

    def _get_all_configurations(self):
        res = self.client.fetch_all('tables/management/configuration', sort={"order": "desc", "column": "lastChange"},
                                    columns=["_id", "sn", "hostname", "lastChange", "lastCheck", "status", "hash"])
        results = defaultdict(list)
        [results[cfg['hostname']].append(Config(**cfg)) for cfg in res]
        self.configs = results

    def _get_managed_ips(self):
        res = self.client.fetch_all('tables/addressing/managed-devs', columns=['ip', 'hostname'],
                                    reports='/technology/addressing/managed-ip')
        self.managed_ip = {ip['ip']: ip['hostname'] for ip in res}

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
        device = self._validate_device(device)
        if not isinstance(date, tuple) and date not in ["$last", "$prev", "$first"]:
            raise SyntaxError("Date must be in [$last, $prev, $first] or tuple ('startDate', 'endDate')")

        if device:
            config_hash, config_date = self._get_hash(self.configs[device], date)
            if config_hash:
                res = self.client.get('/tables/management/configuration/download',
                                      params=dict(hash=config_hash, sanitized=sanitized))
                return Result(timestamp=config_date, text=res.text)
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
                    return cfg.config_hash, cfg.last_change
        elif date == '$last':
            return configs[0].config_hash, configs[0].last_change
        elif date == '$prev' and len(configs) > 1:
            return configs[1].config_hash, configs[1].last_change
        elif date == '$first':
            return configs[-1].config_hash, configs[-1].last_change
        return None, None

    def _validate_device(self, device: str):
        try:
            if IPv4Address(device):
                device = self.managed_ip[device]
        except AddressValueError:
            pass
        except KeyError:
            logger.error(f"IP {device} not found in Managed IP's.")
            return None
        if device not in self.configs:
            logger.error(f"Device {device} not found in Configurations")
            return None
        return device


