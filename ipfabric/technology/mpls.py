import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Mpls(BaseModel):
    client: Any

    @property
    def ldp_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/mpls/ldp/neighbors")

    @property
    def ldp_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/mpls/ldp/interfaces")

    @property
    def rsvp_neighbors(self):
        return models.Table(client=self.client, endpoint="tables/mpls/rsvp/neighbors")

    @property
    def rsvp_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/mpls/rsvp/interfaces")

    @property
    def rsvp_forwarding(self):
        return models.Table(client=self.client, endpoint="tables/mpls/forwarding")

    @property
    def l3vpn_pe_routers(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-routers")

    @property
    def l3vpn_pe_vrfs(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-vrfs")

    @property
    def l3vpn_vrf_targets(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l3-vpn/vrf-targets")

    @property
    def l3vpn_pe_routes(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-routes")

    @property
    def l2vpn_point_to_point_vpws(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l2-vpn/point-to-point-vpws")

    @property
    def l2vpn_point_to_multipoint(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l2-vpn/point-to-multipoint")

    @property
    def l2vpn_circuit_cross_connect(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l2-vpn/curcit-cross-connect")

    @property
    def l2vpn_pseudowires(self):
        return models.Table(client=self.client, endpoint="tables/mpls/l2-vpn/pseudowires")
