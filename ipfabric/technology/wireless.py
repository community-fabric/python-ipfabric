import logging
from pydantic import BaseModel
from typing import Any
from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Wireless(BaseModel):
    client: Any

    @property
    def controllers(self):
        return models.Table(client=self.client, endpoint="tables/wireless/controllers")

    @property
    def access_points(self):
        return models.Table(client=self.client, endpoint="tables/wireless/access-points")

    @property
    def radios_detail(self):
        return models.Table(client=self.client, endpoint="tables/wireless/radio")

    @property
    def radios_ssid_summary(self):
        return models.Table(client=self.client, endpoint="tables/wireless/ssid-summary")

    @property
    def clients(self):
        return models.Table(client=self.client, endpoint="tables/wireless/clients")
