import logging
from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Routing(BaseModel):
    client: Any

    @property
    def summary_protocols(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols")

    @property
    def summary_protocols_bgp(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/bgp")

    @property
    def summary_protocols_eigrp(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/eigrp")

    @property
    def summary_protocols_isis(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/isis")

    @property
    def summary_protocols_ospf(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/ospf")

    @property
    def summary_protocols_ospfv3(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/ospfv3")

    @property
    def summary_protocols_rip(self):
        return models.Table(client=self.client, endpoint="tables/networks/summary/protocols/rip")

    @property
    def routes_ipv4(self):
        return models.Table(client=self.client, endpoint="tables/networks/routes")

    @property
    def routes_ipv6(self):
        return models.Table(client=self.client, endpoint="tables/networks/ipv6-routes")

    @property
    def route_stability(self):
        return models.Table(client=self.client, endpoint="tables/networks/route-stability")

    @property
    def ospf_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/ospf/neighbors")

    @property
    def ospf_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/ospf/interfaces")

    @property
    def ospfv3_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/ospf-v3/neighbors")

    @property
    def ospfv3_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/ospf-v3/interfaces")

    @property
    def bgp_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/bgp/neighbors")

    @property
    def bgp_address_families(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/bgp/address-families")

    @property
    def eigrp_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/eigrp/neighbors")

    @property
    def eigrp_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/eigrp/interfaces")

    @property
    def rip_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/rip/neighbors")

    @property
    def rip_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/rip/interfaces")

    @property
    def isis_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/is-is/neighbors")

    @property
    def isis_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/routing/protocols/is-is/interfaces")

    @property
    def path_lookup_checks(self):
        return models.Table(client=self.client, endpoint="tables/networks/path-lookup-checks")

    @property
    def vrf_summary(self):
        return models.Table(client=self.client, endpoint="tables/vrf/summary")

    @property
    def vrf_detail(self):
        return models.Table(client=self.client, endpoint="tables/vrf/detail")

    @property
    def vrf_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/vrf/interfaces")
