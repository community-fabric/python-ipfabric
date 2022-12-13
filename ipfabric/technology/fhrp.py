import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class Fhrp(BaseModel):
    client: Any

    @property
    def group_state(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/group-state")

    @property
    def group_members(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/group-members")

    @property
    def stproot_alignment(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/stproot-alignment")

    @property
    def balancing(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/balancing")

    @property
    def glbp_forwarders(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/glbp-forwarders")

    @property
    def virtual_gateways(self):
        return models.Table(client=self.client, endpoint="tables/fhrp/virtual-gateways")
