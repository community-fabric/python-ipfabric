from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric import IPFClient

import logging
import httpx
from datetime import datetime
from typing import Optional, List
from pathlib import Path
from time import sleep

from pydantic import BaseModel, Field
from ipfabric.models import Jobs
from urllib.parse import urljoin

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


def snapshot_upload(ipf: IPFClient, file: str):
    file = {'file': (Path(file).name, open(file, 'rb'), 'application/x-tar')}
    resp = httpx.request('POST', urljoin(str(ipf.base_url), 'snapshots/upload'), files=file, auth=ipf.auth,
                         verify=ipf.verify)
    resp.raise_for_status()
    return resp.json()


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
            self.status = "done"
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

    def download(self, ipf: IPFClient, path: str = None, timeout: int = 60, retry: int = 5):
        if not path:
            path = Path(f"{self.snapshot_id}.tar")
        elif not isinstance(path, Path):
            path = Path(f"{path}")
        if not path.name.endswith('.tar'):
            path = Path(f"{path.name}.tar")

        # start download job
        resp = ipf.get(f"/snapshots/{self.snapshot_id}/download")
        resp.raise_for_status()
        job = Jobs(client=ipf)

        # waiting for download job to process
        sleep(timeout)  # TODO How do we handle waiting and retry? Should we move timeout also to Job?
        job_id = job.get_snapshot_download_job_id(self.snapshot_id, retry=retry)
        file = ipf.get(f"jobs/{job_id}/download")
        with open(path, "wb") as fp:
            fp.write(file.read())
        return path
