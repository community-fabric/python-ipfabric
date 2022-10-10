import logging
from collections import defaultdict
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from typing import Any, Union, Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from ipfabric.tools.shared import date_parser

logger = logging.getLogger("python-ipfabric")


class Config(BaseModel):
    config_id: str = Field(alias="id")
    sn: str
    hostname: str
    config_hash: str = Field(alias="hash")
    status: str
    last_change: datetime = Field(alias="lastChangeAt")
    last_check: datetime = Field(alias="lastCheckAt")
    text: Optional[str] = None


@dataclass
class DeviceConfigs:
    ipf: Any

    def get_all_configurations(self, device: Optional[str] = None, sn: Optional[str] = None):
        """
        Get all configurations in IP Fabric
        :param device: str: Hostname (case sensitive) filter
        :param sn: str: Serial number of device
        :return: dict: {sn: [Config, Config]}
        """
        if device or sn:
            filters = dict(sn=["eq", sn]) if sn else dict(hostname=["ieq", device])
            res = self.ipf.fetch_all(
                "tables/management/configuration",
                sort={"order": "desc", "column": "lastChangeAt"},
                columns=[
                    "id",
                    "sn",
                    "hostname",
                    "lastChangeAt",
                    "lastCheckAt",
                    "status",
                    "hash",
                ],
                filters=filters,
                snapshot=False,
            )
            if len(res) == 0:
                logger.warning(f"Could not find any configurations for device '{device}'.")
                return None
        else:
            res = self.ipf.fetch_all(
                "tables/management/configuration",
                sort={"order": "desc", "column": "lastChangeAt"},
                columns=[
                    "id",
                    "sn",
                    "hostname",
                    "lastChangeAt",
                    "lastCheckAt",
                    "status",
                    "hash",
                ],
                snapshot=False,
            )
        results = defaultdict(list)
        [results[cfg["sn"]].append(Config(**cfg)) for cfg in res]
        return results

    def _search_ip(self, ip: str, snapshot_id: str = None, log: bool = False) -> dict:
        res = self.ipf.fetch_all(
            "tables/addressing/managed-devs",
            columns=["ip", "hostname", "sn"],
            reports="/technology/addressing/managed-ip",
            filters=dict(ip=["eq", ip]),
        )
        if len(res) == 1 and not log:
            return {"hostname": res[0]["hostname"], "sn": res[0]["sn"]}
        if len(res) == 1 and log:
            res = self.ipf.inventory.devices.all(
                columns=["hostname", "taskKey", "sn"],
                snapshot_id=snapshot_id,
                filters=dict(sn=["eq", res[0]["sn"]]),
            )
            return {"hostname": res[0]["hostname"], "taskKey": res[0]["taskKey"], "sn": res[0]["sn"]}
        elif len(res) > 1:
            logger.warning(f"Found multiple entries for IP '{ip}'.")
        elif len(res) == 0:
            logger.warning(f"Could not find a matching IP for '{ip}'.")
        return {"hostname": None, "sn": None}

    def get_configuration(
        self, device: str = None, sn: str = None, sanitized: bool = True, date: Union[str, tuple] = "$last"
    ):
        """
        Gets last configuration of a device based on hostname or IP or IPF Unique Serial Number
        :param device: str: Hostname or IP
        :param sn: str: Serial Number
        :param sanitized: bool: Default True to mask passwords
        :param date: Union[str, tuple]: Defaults to latest config. Values in [$last, $prev, $first] or can be a
                                        tuple of a date range to get the latest snapshot in that range.
                                        Date can be string or int in seconds ("11/22/ 1:30", 1637629200)
        :return: Result: Returns a result or None
        """
        if not isinstance(date, tuple) and date not in ["$last", "$prev", "$first"]:
            raise SyntaxError("Date must be in [$last, $prev, $first] or tuple ('startDate', 'endDate')")
        if not sn:
            sn = self._validate_device(device)["sn"]
            if not sn:
                return None
        cfgs = self.get_all_configurations(sn=sn)
        if not cfgs:
            return None
        cfg = self._get_hash(cfgs[sn], date)
        if cfg:
            return self.get_text_config(cfg, sanitized)
        else:
            logger.error(f"Could not find a configuration with date {date}")
            return None

    def get_text_config(self, cfg: Config, sanitized: bool = True):
        res = self.ipf.get(
            "/tables/management/configuration/download",
            params=dict(hash=cfg.config_hash, sanitized=sanitized),
        )
        res.raise_for_status()
        cfg.text = res.text
        return cfg

    @staticmethod
    def _get_hash(configs, date):
        if isinstance(date, tuple):
            start = date_parser(date[0])
            end = date_parser(date[1])
            for cfg in configs:
                if start < cfg.last_change < end:
                    return cfg
        elif date == "$last":
            return configs[0]
        elif date == "$prev" and len(configs) > 1:
            return configs[1]
        elif date == "$first":
            return configs[-1]
        return None

    def _validate_device(self, device: str, snapshot_id: str = None, log: bool = False) -> dict:
        try:
            if IPv4Address(device):
                return self._search_ip(device, snapshot_id=snapshot_id, log=log)
        except AddressValueError:
            pass
        res = self.ipf.inventory.devices.all(
            columns=["hostname", "taskKey", "sn"],
            filters=dict(hostname=["ieq", device]),
            snapshot_id=snapshot_id,
        )
        if len(res) == 1:
            return {"hostname": res[0]["hostname"], "taskKey": res[0]["taskKey"], "sn": res[0]["sn"]}
        elif len(res) == 0:
            logger.warning(f"Could not find a matching device for '{device}'")
        elif len(res) > 1:
            logger.warning(f"Found multiple devices matching '{device}'.")
        return {"hostname": None, "sn": None}

    def get_log(self, device: str, snapshot_id: str = None):
        device = self._validate_device(device, snapshot_id=snapshot_id, log=True)
        if not device["sn"]:
            return None
        return self.get_text_log(device)

    def get_text_log(self, device: dict):
        res = self.ipf.get("/os/logs/task/" + device["taskKey"])
        res.raise_for_status()
        return res.text
