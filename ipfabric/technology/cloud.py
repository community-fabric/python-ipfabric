import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class Cloud(BaseModel):
    client: Any

    @property
    def virtual_machines(self):
        return models.Table(client=self.client, endpoint="tables/cloud/virtual-machines")

    @property
    def virtual_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/cloud/virtual-machines-interfaces")
