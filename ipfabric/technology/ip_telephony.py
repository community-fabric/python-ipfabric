import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class IpTelephony(BaseModel):
    client: Any

    @property
    def phones(self):
        return models.Table(client=self.client, endpoint="tables/inventory/phones")
