import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Platforms(BaseModel):
    client: Any

    @property
    def environment_power_supplies(self):
        return models.Table(client=self.client, endpoint="tables/inventory/power-supplies")

    @property
    def environment_power_supplies_fans(self):
        return models.Table(client=self.client, endpoint="tables/inventory/power-supplies-fans")

    @property
    def environment_fans(self):
        return models.Table(client=self.client, endpoint="tables/inventory/fans")

    @property
    def environment_modules(self):
        return models.Table(client=self.client, endpoint="tables/inventory/modules")

    @property
    def juniper_cluster(self):
        return models.Table(client=self.client, endpoint="tables/platforms/cluster/srx")

    @property
    def cisco_fex_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/platforms/fex/interfaces")

    @property
    def cisco_fex_modules(self):
        return models.Table(client=self.client, endpoint="tables/platforms/fex/modules")

    @property
    def cisco_vdc_devices(self):
        return models.Table(client=self.client, endpoint="tables/platforms/vdc/devices")

    @property
    def platform_cisco_vss(self):
        return models.Table(client=self.client, endpoint="tables/platforms/vss/overview")

    @property
    def cisco_vss_chassis(self):
        return models.Table(client=self.client, endpoint="tables/platforms/vss/chassis")

    @property
    def cisco_vss_vsl(self):
        return models.Table(client=self.client, endpoint="tables/platforms/vss/vsl")

    @property
    def poe_devices(self):
        return models.Table(client=self.client, endpoint="tables/platforms/poe/devices")

    @property
    def poe_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/platforms/poe/interfaces")

    @property
    def poe_modules(self):
        return models.Table(client=self.client, endpoint="tables/platforms/poe/modules")

    @property
    def stacks(self):
        return models.Table(client=self.client, endpoint="tables/platforms/stacks")

    @property
    def stacks_members(self):
        return models.Table(client=self.client, endpoint="tables/platforms/stack/members")

    @property
    def stacks_stack_ports(self):
        return models.Table(client=self.client, endpoint="tables/platforms/stack/connections")
