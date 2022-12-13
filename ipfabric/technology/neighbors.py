import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class Neighbors(BaseModel):
    client: Any

    @property
    def neighbors_all(self):
        return models.Table(client=self.client, endpoint="tables/neighbors/all")

    @property
    def neighbors_unmanaged(self):
        return models.Table(client=self.client, endpoint="tables/neighbors/unmanaged")

    @property
    def neighbors_unidirectional(self):
        return models.Table(client=self.client, endpoint="tables/neighbors/unidirectional")

    @property
    def neighbors_endpoints(self):
        return models.Table(client=self.client, endpoint="tables/neighbors/endpoints")
