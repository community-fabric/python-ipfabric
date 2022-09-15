import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Security(BaseModel):
    client: Any

    @property
    def acl(self):
        return models.Table(client=self.client, endpoint="tables/security/acl")

    @property
    def acl_interface(self):
        return models.Table(client=self.client, endpoint="tables/security/acl/interfaces")

    @property
    def acl_global_policies(self):
        return models.Table(client=self.client, endpoint="tables/security/acl/global-policies")

    @property
    def dmvpn(self):
        return models.Table(client=self.client, endpoint="tables/security/dmvpn")

    @property
    def dhcp_snooping(self):
        return models.Table(client=self.client, endpoint="tables/security/dhcp/snooping")

    @property
    def dhcp_snooping_bindings(self):
        return models.Table(client=self.client, endpoint="tables/security/dhcp/bindings")

    @property
    def ipsec_tunnels(self):
        return models.Table(client=self.client, endpoint="tables/security/ipsec/tunnels")

    @property
    def ipsec_gateways(self):
        return models.Table(client=self.client, endpoint="tables/security/ipsec/gateways")

    @property
    def secure_ports_devices(self):
        return models.Table(client=self.client, endpoint="tables/security/secure-ports/devices")

    @property
    def secure_ports_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/security/secure-ports/interfaces")

    @property
    def secure_ports_users(self):
        return models.Table(client=self.client, endpoint="tables/security/secure-ports/users")

    @property
    def zone_firewall_policies(self):
        return models.Table(client=self.client, endpoint="tables/security/zone-firewall/policies")

    @property
    def zone_firewall_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/security/zone-firewall/interfaces")
