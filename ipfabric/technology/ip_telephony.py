import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class IpTelephony(BaseModel):
    client: Any

    @property
    def phones(self):
        return models.Table(client=self.client, endpoint="tables/inventory/phones")
