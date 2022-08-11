import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger()


class ManagedNetworks(BaseModel):
    client: Any

    @property
    def networks(self):
        return models.Table(client=self.client, endpoint="tables/networks")

    @property
    def gateway_redundancy(self):
        return models.Table(client=self.client, endpoint="tables/networks/gateway-redundancy")
