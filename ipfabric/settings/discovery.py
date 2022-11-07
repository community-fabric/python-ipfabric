import logging
from typing import Any

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")


class Networks(BaseModel):
    exclude: list[str]
    include: list[str]


@dataclass
class Discovery:
    client: Any

    @property
    def networks(self):
        res = self.client.get("settings")
        res.raise_for_status()
        return Networks(**res.json()["networks"])

    def update_discovery_networks(self, subnets: list, include: bool = False):
        payload = dict()
        payload["networks"] = dict()
        if include:
            payload["networks"]["include"] = subnets
            payload["networks"]["exclude"] = self.networks.exclude
        else:
            payload["networks"]["exclude"] = subnets
            payload["networks"]["include"] = self.networks.include
        res = self.client.patch("settings", json=payload)
        res.raise_for_status()
        return Networks(**res.json()["networks"])
