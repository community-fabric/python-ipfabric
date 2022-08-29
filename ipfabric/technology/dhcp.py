import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Dhcp(BaseModel):
    client: Any

    @property
    def relay_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/interfaces")

    @property
    def relay_interfaces_stats_received(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/received")

    @property
    def relay_interfaces_stats_relayed(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/relayed")

    @property
    def relay_interfaces_stats_sent(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/sent")

    @property
    def relay_global_stats_summary(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/summary")

    @property
    def relay_global_stats_received(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/received")

    @property
    def relay_global_stats_relayed(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/relayed")

    @property
    def relay_global_stats_sent(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/sent")

    @property
    def server_summary(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/server/summary")

    @property
    def server_pools(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/server/pools")

    @property
    def server_leases(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/server/leases")

    @property
    def server_excluded_ranges(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/server/excluded-ranges")

    @property
    def server_excluded_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/dhcp/server/interfaces")
