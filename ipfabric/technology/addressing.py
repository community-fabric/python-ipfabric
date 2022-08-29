import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Addressing(BaseModel):
    client: Any

    @property
    def arp_table(self):
        return models.Table(client=self.client, endpoint="tables/addressing/arp")

    @property
    def mac_table(self):
        return models.Table(client=self.client, endpoint="tables/addressing/mac")

    @property
    def managed_ip_ipv4(self):
        return models.Table(client=self.client, endpoint="tables/addressing/managed-devs")

    @property
    def managed_ip_ipv6(self):
        return models.Table(client=self.client, endpoint="tables/addressing/ipv6-managed-devs")

    @property
    def managed_duplicate_ip(self):
        return models.Table(client=self.client, endpoint="tables/addressing/duplicate-ip")

    @property
    def nat_rules(self):
        return models.Table(client=self.client, endpoint="tables/addressing/nat/rules")

    @property
    def nat_pools(self):
        return models.Table(client=self.client, endpoint="tables/addressing/nat/pools")

    @property
    def ipv6_neighbor_discovery(self):
        return models.Table(client=self.client, endpoint="tables/addressing/ipv6-neighbors")
