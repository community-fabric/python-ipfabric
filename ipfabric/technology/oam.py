import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Oam(BaseModel):
    client: Any

    @property
    def unidirectional_link_detection_neighbors(self):
        return models.Table(
            client=self.client, endpoint="tables/management/oam/unidirectional-link-detection/neighbors"
        )

    @property
    def unidirectional_link_detection_interfaces(self):
        return models.Table(
            client=self.client, endpoint="tables/management/oam/unidirectional-link-detection/interfaces"
        )
