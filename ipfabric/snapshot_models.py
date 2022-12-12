from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric import IPFClient
    from ipfabric.api import IPFabricAPI

import logging
from datetime import datetime
from typing import Optional, List, Union
from httpx import HTTPError

from pydantic import BaseModel, Field

logger = logging.getLogger("python-ipfabric")

SNAPSHOT_COLUMNS = [
    "id",
    "status",
    "finishStatus",
    "loadedSize",
    "unloadedSize",
    "name",
    "note",
    "sites",
    "fromArchive",
    "loading",
    "locked",
    "deviceAddedCount",
    "deviceRemovedCount",
    "interfaceActiveCount",
    "interfaceCount",
    "interfaceEdgeCount",
    "totalDevCount",
    "isLastSnapshot",
    "tsChange",
    "tsEnd",
    "tsStart",
    "userCount",
]


class Error(BaseModel):
    error_type: str = Field(alias="errorType")
    count: int


class Snapshot(BaseModel):
    snapshot_id: str = Field(alias="id")
    name: Optional[str]
    note: Optional[str]
    total_dev_count: int = Field(alias="totalDevCount")
    licensed_dev_count: Optional[int] = Field(alias="licensedDevCount")
    user_count: int = Field(alias="userCount")
    interface_active_count: int = Field(alias="interfaceActiveCount")
    interface_count: int = Field(alias="interfaceCount")
    interface_edge_count: int = Field(alias="interfaceEdgeCount")
    device_added_count: int = Field(alias="deviceAddedCount")
    device_removed_count: int = Field(alias="deviceRemovedCount")
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
    loaded_size: int = Field(alias="loadedSize")
    unloaded_size: int = Field(alias="unloadedSize")
    disabled_graph_cache: Optional[bool]
    disabled_historical_data: Optional[bool]
    disabled_intent_verification: Optional[bool]

    def lock(self, ipf: IPFClient):
        if not self.locked and self.loaded:
            res = ipf.post(f"snapshots/{self.snapshot_id}/lock")
            res.raise_for_status()
            self.locked = True
        elif not self.loaded:
            logger.error(f"Snapshot {self.snapshot_id} is not loaded.")
            return False
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already locked.")
        return True

    def unlock(self, ipf: IPFClient):
        if self.locked and self.loaded:
            res = ipf.post(f"snapshots/{self.snapshot_id}/unlock")
            res.raise_for_status()
            self.locked = False
        elif not self.loaded:
            logger.error(f"Snapshot {self.snapshot_id} is not loaded.")
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already unlocked.")
        return True

    @property
    def loaded(self):
        return self.status == "done" and self.finish_status == "done"

    def unload(self, ipf: IPFClient):
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
            self.status = "unloaded"
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already unloaded.")
        return True

    def load(self, ipf: IPFClient):
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
            self.get_assurance_engine_settings(ipf)
            self.status = "done"  # TODO: Implement check to know when snapshot is done loading
        else:
            logger.warning(f"Snapshot {self.snapshot_id} is already loaded.")
        return True

    def attributes(self, ipf: IPFClient):
        """
        Load Snapshot
        :param ipf: IPFClient
        :return: True
        """
        return ipf.fetch_all("tables/snapshot-attributes", snapshot_id=self.snapshot_id)

    def get_snapshot_settings(self, ipf: Union[IPFClient, IPFabricAPI]):
        res = ipf.get(f"/snapshots/{self.snapshot_id}/settings")
        try:
            res.raise_for_status()
            return res.json()
        except HTTPError:
            logger.warning("User/Token does not have access to `snapshots/:key/settings`; "
                           "cannot get status of Assurance Engine tasks.")
        return None

    def get_assurance_engine_settings(self, ipf: Union[IPFClient, IPFabricAPI]):
        settings = self.get_snapshot_settings(ipf)
        if settings is None:
            logger.warning(f"Could not get Snapshot {self.snapshot_id} Settings to verify Assurance Engine tasks.")
            return None
        disabled = settings.get('disabledPostDiscoveryActions', list())
        self.disabled_graph_cache = True if "graphCache" in disabled else False
        self.disabled_historical_data = True if "historicalData" in disabled else False
        self.disabled_intent_verification = True if "intentVerification" in disabled else False
        return dict(disabled_graph_cache=self.disabled_graph_cache,
                    disabled_historical_data=self.disabled_historical_data,
                    disabled_intent_verification=self.disabled_intent_verification)

    def update_assurance_engine_settings(
            self,
            ipf: Union[IPFClient, IPFabricAPI],
            disable_graph_cache: bool = False,
            disable_historical_data: bool = False,
            disable_intent_verification: bool = False
    ):
        settings = self.get_snapshot_settings(ipf)
        if settings is None:
            logger.warning(f"Could not get Snapshot {self.snapshot_id} Settings and "
                           f"cannot update Assurance Engine tasks.")
            return False
        disabled = list()
        if disable_graph_cache:
            disabled.append("graphCache")
        if disable_historical_data:
            disabled.append("historicalData")
        if disable_intent_verification:
            disabled.append("intentVerification")
        if set(disabled) == set(settings.get('disabledPostDiscoveryActions', list())):
            logger.info("No changes to Assurance Engine Settings required.")
            return True
        res = ipf.patch(f"/snapshots/{self.snapshot_id}/settings", json=dict(disabledPostDiscoveryActions=disabled))
        res.raise_for_status()  # TODO: Implement check to know when snapshot is done calculations
        return True
