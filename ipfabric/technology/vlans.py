import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Vlans(BaseModel):
    client: Any

    @property
    def device_summary(self):
        return models.Table(client=self.client, endpoint="tables/vlan/device-summary")

    @property
    def device_detail(self):
        return models.Table(client=self.client, endpoint="tables/vlan/device")

    @property
    def network_summary(self):
        return models.Table(client=self.client, endpoint="tables/vlan/network-summary")

    @property
    def site_summary(self):
        return models.Table(client=self.client, endpoint="tables/vlan/site-summary")

    @property
    def l3_gateways(self):
        return models.Table(client=self.client, endpoint="tables/vlan/l3-gateways")
