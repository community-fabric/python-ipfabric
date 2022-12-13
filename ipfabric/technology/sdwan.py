import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class Sdwan(BaseModel):
    client: Any

    @property
    def sites(self):
        return models.Table(client=self.client, endpoint="tables/sdwan/sites")

    @property
    def links(self):
        return models.Table(client=self.client, endpoint="tables/sdwan/links")
