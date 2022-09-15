import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Sdn(BaseModel):
    client: Any

    @property
    def aci_endpoints(self):
        return models.Table(client=self.client, endpoint="tables/aci/endpoints")

    @property
    def aci_vlan(self):
        return models.Table(client=self.client, endpoint="tables/aci/vlan")

    @property
    def aci_vrf(self):
        return models.Table(client=self.client, endpoint="tables/aci/vtep")

    @property
    def aci_dtep(self):
        return models.Table(client=self.client, endpoint="tables/aci/dtep")

    @property
    def vxlan_vtep(self):
        return models.Table(client=self.client, endpoint="tables/vxlan/vtep")

    @property
    def vxlan_peers(self):
        return models.Table(client=self.client, endpoint="tables/vxlan/peers")

    @property
    def vxlan_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/vxlan/interfaces")

    @property
    def vxlan_vni(self):
        return models.Table(client=self.client, endpoint="tables/vxlan/vni")

    @property
    def apic_controllers(self):
        return models.Table(client=self.client, endpoint="tables/apic/controllers")

    @property
    def apic_contexts(self):
        return models.Table(client=self.client, endpoint="tables/apic/contexts")

    @property
    def apic_bridge_domains(self):
        return models.Table(client=self.client, endpoint="tables/apic/bridge-domains")

    @property
    def apic_applications(self):
        return models.Table(client=self.client, endpoint="tables/apic/applications")

    @property
    def apic_endpoint_groups(self):
        return models.Table(client=self.client, endpoint="tables/apic/endpoint-groups")

    @property
    def apic_endpoint_groups_contracts(self):
        return models.Table(client=self.client, endpoint="tables/apic/endpoint-groups/contracts")

    @property
    def apic_contracts(self):
        return models.Table(client=self.client, endpoint="tables/apic/contracts")
