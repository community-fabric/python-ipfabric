import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Multicast(BaseModel):
    client: Any

    @property
    def pim_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/neighbors")

    @property
    def pim_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/neighbors")

    @property
    def mroute_overview(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/overview")

    @property
    def mroute_table(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/table")

    @property
    def mroute_oil_detail(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/outgoing-interfaces")

    @property
    def mroute_counters(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/counters")

    @property
    def mroute_first_hop_router(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/first-hop-router")

    @property
    def mroute_sources(self):
        return models.Table(client=self.client, endpoint="tables/multicast/routes/sources")

    @property
    def igmp_groups(self):
        return models.Table(client=self.client, endpoint="tables/multicast/igmp/groups")

    @property
    def igmp_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/multicast/igmp/interfaces")

    @property
    def igmp_snooping_global_config(self):
        return models.Table(client=self.client, endpoint="tables/multicast/igmp/snooping/global")

    @property
    def igmp_snooping_groups(self):
        return models.Table(client=self.client, endpoint="tables/multicast/igmp/snooping/groups")

    @property
    def igmp_snooping_vlans(self):
        return models.Table(client=self.client, endpoint="tables/multicast/igmp/snooping/vlans")

    @property
    def mac_table(self):
        return models.Table(client=self.client, endpoint="tables/multicast/mac")

    @property
    def rp_overview(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/rp/overview")

    @property
    def rp_bsr(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/rp/bsr")

    @property
    def rp_mappings(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/rp/mappings")

    @property
    def rp_mappings_groups(self):
        return models.Table(client=self.client, endpoint="tables/multicast/pim/rp/mappings-groups")
