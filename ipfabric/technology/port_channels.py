import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class PortChannels(BaseModel):
    client: Any

    @property
    def inbound_balancing_table(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/port-channel/balance/inbound")

    @property
    def outbound_balancing_table(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/port-channel/balance/outbound")

    @property
    def member_status_table(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/port-channel/member-status")

    @property
    def mlag_switches(self):
        return models.Table(client=self.client, endpoint="tables/platforms/mlag/switches")

    @property
    def mlag_peers(self):
        return models.Table(client=self.client, endpoint="tables/platforms/mlag/peers")

    @property
    def mlag_pairs(self):
        return models.Table(client=self.client, endpoint="tables/platforms/mlag/pairs")

    @property
    def mlag_cisco_vpc(self):
        return models.Table(client=self.client, endpoint="tables/platforms/mlag/vpc")
