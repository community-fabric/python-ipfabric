import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Stp(BaseModel):
    client: Any

    @property
    def stability(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/topology")

    @property
    def bridges(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/bridges")

    @property
    def instances(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/instances")

    @property
    def vlans(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/vlans")

    @property
    def ports(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/ports")

    @property
    def neighbors(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/neighbors")

    @property
    def guards(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/guards")

    @property
    def inconsistencies(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/inconsistencies/summary")

    @property
    def inconsistencies_details(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/inconsistencies/details")

    @property
    def inconsistencies_ports_vlan_mismatch(self):
        return models.Table(
            client=self.client, endpoint="tables/spanning-tree/inconsistencies/neighbor-ports-vlan-mismatch"
        )

    @property
    def inconsistencies_ports_multiple_neighbors(self):
        return models.Table(
            client=self.client, endpoint="tables/spanning-tree/inconsistencies/ports-multiple-neighbors"
        )

    @property
    def inconsistencies_stp_cdp_ports_mismatch(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/inconsistencies/stp-cdp-ports-mismatch")

    @property
    def inconsistencies_multiple_stp(self):
        return models.Table(client=self.client, endpoint="tables/spanning-tree/inconsistencies/multiple-stp")
