from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field


class Site(BaseModel):
    site_name: str = Field(alias='siteName')
    uid: str
    site_id: str = Field(alias='id')


class Error(BaseModel):
    error_type: str = Field(alias='errorType')
    count: int


class Snapshot(BaseModel):
    snapshot_id: str = Field(alias="id")
    name: Optional[str]
    count: int = Field(alias="totalDevCount")
    state: str
    locked: bool
    start: datetime = Field(alias="tsStart")
    end: Optional[datetime] = Field(alias="tsEnd")
    version: str
    sites: List[Site]
    errors: Optional[List[Error]]

    @property
    def loaded(self):
        return self.state == 'loaded'


class Table(BaseModel):
    endpoint: str
    client: Any

    @property
    def name(self):
        return self.endpoint.split('/')[-1]

    def all(
            self,
            columns: list = None,
            filters: dict = None,
            snapshot_id: Optional[str] = None,
            reports: Optional[str] = None
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :param reports: str: String of frontend URL where the reports are displayed
        :return: list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.endpoint,
            columns=columns,
            filters=filters,
            snapshot_id=snapshot_id,
            reports=reports
        )


class Inventory(BaseModel):
    client: Any

    @property
    def sites(self):
        return Table(client=self.client, endpoint='/tables/inventory/sites')

    @property
    def vendors(self):
        return Table(client=self.client, endpoint='/tables/inventory/summary/vendors')

    @property
    def devices(self):
        return Table(client=self.client, endpoint='/tables/inventory/devices')

    @property
    def models(self):
        return Table(client=self.client, endpoint='/tables/inventory/summary/models')

    @property
    def platforms(self):
        return Table(client=self.client, endpoint='/tables/inventory/summary/platforms')

    @property
    def pn(self):
        return Table(client=self.client, endpoint='/tables/inventory/pn')

    @property
    def families(self):
        return Table(client=self.client, endpoint='/tables/inventory/summary/families')

    @property
    def interfaces(self):
        return Table(client=self.client, endpoint='/tables/inventory/interfaces')
