from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field


class Site(BaseModel):
    _sitename: str = Field(alias="siteName")
    _name: str = Field(alias="name")
    uid: str
    site_id: Optional[str] = Field(None, alias="id")

    @property
    def site_name(self):
        return self._name or self._sitename


class Error(BaseModel):
    error_type: str = Field(alias="errorType")
    count: int


class Snapshot(BaseModel):
    snapshot_id: str = Field(alias="id")
    name: Optional[str]
    count: int = Field(alias="totalDevCount")
    licensed_count: int = Field(alias="licensedDevCount")
    status: str
    state: str
    locked: bool
    start: datetime = Field(alias="tsStart")
    end: Optional[datetime] = Field(alias="tsEnd")
    version: Optional[str] = None
    sites: List[Site]
    errors: Optional[List[Error]]

    @property
    def loaded(self):
        return self.state == "loaded"


class Table(BaseModel):
    endpoint: str
    client: Any

    @property
    def name(self):
        return self.endpoint.split("/")[-1]

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :return: list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.endpoint,
            columns=columns,
            filters=filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
        )


class Inventory(BaseModel):
    client: Any

    @property
    def sites(self):
        return Table(client=self.client, endpoint="/tables/inventory/sites")

    @property
    def vendors(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/vendors")

    @property
    def devices(self):
        return Table(client=self.client, endpoint="/tables/inventory/devices")

    @property
    def models(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/models")

    @property
    def platforms(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/platforms")

    @property
    def pn(self):
        return Table(client=self.client, endpoint="/tables/inventory/pn")

    @property
    def families(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/families")

    @property
    def interfaces(self):
        return Table(client=self.client, endpoint="/tables/inventory/interfaces")

    @property
    def hosts(self):
        return Table(client=self.client, endpoint="tables/addressing/hosts")
