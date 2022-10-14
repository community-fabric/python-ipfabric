import logging
from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field

from ipfabric.technology import *

logger = logging.getLogger("python-ipfabric")

SNAPSHOT_COLUMNS = ['id', 'status', 'finishStatus', 'loadedSize', 'unloadedSize', 'name', 'note', 'sites',
                    'fromArchive', 'loading', 'locked', 'deviceAddedCount', 'deviceRemovedCount',
                    'interfaceActiveCount', 'interfaceCount', 'interfaceEdgeCount', 'totalDevCount',
                    'isLastSnapshot', 'tsChange', 'tsEnd', 'tsStart', 'userCount']


class Error(BaseModel):
    error_type: str = Field(alias="errorType")
    count: int


class Snapshot(BaseModel):
    snapshot_id: str = Field(alias="id")
    name: Optional[str]
    note: Optional[str]
    total_dev_count: int = Field(alias="totalDevCount")
    licensed_dev_count: Optional[int] = Field(alias="licensedDevCount")
    user_count: int = Field(alias='userCount')
    interface_active_count: int = Field(alias="interfaceActiveCount")
    interface_count: int = Field(alias="interfaceCount")
    interface_edge_count: int = Field(alias='interfaceEdgeCount')
    device_added_count: int = Field(alias="deviceAddedCount")
    device_removed_count: int = Field(alias='deviceRemovedCount')
    status: str
    finish_status: str = Field(alias="finishStatus")
    loading: bool
    locked: bool
    from_archive: bool = Field(alias="fromArchive")
    start: datetime = Field(alias="tsStart")
    end: Optional[datetime] = Field(alias="tsEnd")
    change: Optional[datetime] = Field(alias="tsChange")
    version: Optional[str] = None
    initial_version: Optional[str] = Field(alias="initialVersion")
    sites: List[str]
    errors: Optional[List[Error]]
    loaded_size: int = Field(alias='loadedSize')
    unloaded_size: int = Field(alias='unloadedSize')

    def lock(self, ipf):
        if not self.locked and self.loaded:
            res = ipf.post(f'snapshots/{self.snapshot_id}/lock')
            res.raise_for_status()
        elif not self.loaded:
            logger.error(f"Snapshot {self.snapshot_id} is not loaded.")
            return False
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already locked.")
        return True

    def unlock(self, ipf):
        if self.locked and self.loaded:
            res = ipf.post(f'snapshots/{self.snapshot_id}/unlock')
            res.raise_for_status()
        elif not self.loaded:
            logger.error(f"Snapshot {self.snapshot_id} is not loaded.")
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already unlocked.")
        return True

    @property
    def loaded(self):
        return self.status == "done" and self.finish_status == "done"

    def unload(self, ipf):
        """
        Load Snapshot
        :param ipf: IPFClient
        :return: True
        """
        if self.loaded:
            res = ipf.post(
                "snapshots/unload", json=[dict(jobDetail=int(datetime.now().timestamp() * 1000), id=self.snapshot_id)]
            )
            res.raise_for_status()
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already unloaded.")
        return True

    def load(self, ipf):
        """
        Load Snapshot
        :param ipf: IPFClient
        :return: True
        """
        if not self.loaded:
            res = ipf.post(
                "snapshots/load", json=[dict(jobDetail=int(datetime.now().timestamp() * 1000), id=self.snapshot_id)]
            )
            res.raise_for_status()
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already loaded.")
        return True

    def attributes(self, ipf):
        """
        Load Snapshot
        :param ipf: IPFClient
        :return: True
        """
        return ipf.fetch_all("tables/snapshot-attributes", snapshot_id=self.snapshot_id)


class Table(BaseModel):
    endpoint: str
    client: Any

    @property
    def name(self):
        return self.endpoint.split("/")[-1]

    def fetch(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :param limit: int: Default to 1,000 rows
        :param start: int: Starts at 0
        :return: list: List of Dictionaries
        """
        return self.client.fetch(
            self.endpoint,
            columns=columns,
            filters=filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            limit=limit,
            start=start,
        )

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

    def count(self, filters: Optional[dict] = None, snapshot_id: Optional[str] = None):
        """
        Gets count of table
        :param filters: dict: Optional filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :return: int: Count
        """
        return self.client.get_count(
            self.endpoint,
            filters=filters,
            snapshot_id=snapshot_id,
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

    @property
    def phones(self):
        return Table(client=self.client, endpoint="tables/inventory/phones")

    @property
    def fans(self):
        return Table(client=self.client, endpoint="tables/inventory/fans")

    @property
    def modules(self):
        return Table(client=self.client, endpoint="tables/inventory/modules")

    @property
    def powerSupplies(self):
        logger.warning(
            """Use of client.inventory.PowerSupplies will be deprecated in a future release, please 
                        use client.technology.platform_environment_power_supplies"""
        )
        return Table(client=self.client, endpoint="tables/inventory/power-supplies")

    @property
    def powerSuppliesFans(self):
        logger.warning(
            """Use of client.inventory.PowerSuppliesFans will be deprecated in a future release, please 
                        use client.technology.platform_environment_power_supplies_fans"""
        )
        return Table(client=self.client, endpoint="tables/inventory/power-supplies-fans")


class Technology(BaseModel):
    client: Any

    @property
    def platforms(self):
        return Platforms(client=self.client)

    @property
    def interfaces(self):
        return Interfaces(client=self.client)

    @property
    def neighbors(self):
        return Neighbors(client=self.client)

    @property
    def dhcp(self):
        return Dhcp(client=self.client)

    @property
    def port_channels(self):
        return PortChannels(client=self.client)

    @property
    def vlans(self):
        return Vlans(client=self.client)

    @property
    def stp(self):
        return Stp(client=self.client)

    @property
    def addressing(self):
        return Addressing(client=self.client)

    @property
    def fhrp(self):
        return Fhrp(client=self.client)

    @property
    def managed_networks(self):
        return ManagedNetworks(client=self.client)

    @property
    def mpls(self):
        return Mpls(client=self.client)

    @property
    def multicast(self):
        return Multicast(client=self.client)

    @property
    def cloud(self):
        return Cloud(client=self.client)

    @property
    def management(self):
        return Management(client=self.client)

    @property
    def ip_telephony(self):
        return IpTelephony(client=self.client)

    @property
    def load_balancing(self):
        return LoadBalancing(client=self.client)

    @property
    def oam(self):
        return Oam(client=self.client)

    @property
    def qos(self):
        return Qos(client=self.client)

    @property
    def routing(self):
        return Routing(client=self.client)

    @property
    def sdn(self):
        return Sdn(client=self.client)

    @property
    def sdwan(self):
        return Sdwan(client=self.client)

    @property
    def security(self):
        return Security(client=self.client)

    @property
    def wireless(self):
        return Wireless(client=self.client)
