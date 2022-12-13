from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric import IPFClient
    from ipfabric.api import IPFabricAPI

import logging
import httpx
from datetime import datetime
from typing import Optional, List, Union
from httpx import HTTPError
from pathlib import Path

from pydantic import BaseModel, Field
from ipfabric.models import Jobs
from urllib.parse import urljoin

logger = logging.getLogger("ipfabric")

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


def snapshot_upload(ipf: IPFClient, filename: str):
    data = {"file": (Path(filename).name, open(filename, "rb"), "application/x-tar")}
    resp = httpx.request(
        "POST", urljoin(str(ipf.base_url), "snapshots/upload"), files=data, auth=ipf.auth, verify=ipf.verify
    )
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

    def unload(self, ipf: IPFClient, wait_for_unload: bool = False, timeout: int = 60, retry: int = 5):
        if not self.loaded:
            logger.warning(f"Snapshot {self.snapshot_id} is already unloaded.")
        ts = int(datetime.now().timestamp() * 1000)
        res = ipf.post("snapshots/unload", json=[dict(jobDetail=ts, id=self.snapshot_id)])
        res.raise_for_status()
        if wait_for_unload:
            job = Jobs(client=ipf)
            if not job.check_snapshot_unload_job(self.snapshot_id, ts, retry, timeout):
                logger.error("Snapshot Unload did not finish.")
                return False
        self._refresh_status(ipf)
        return True

    def load(
        self,
        ipf: IPFClient,
        wait_for_load: bool = True,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ):

        if self.loaded:
            logger.warning(f"Snapshot {self.snapshot_id} is already loaded.")
            return True
        ts = int(datetime.now().timestamp() * 1000)
        res = ipf.post("snapshots/load", json=[dict(jobDetail=ts, id=self.snapshot_id)])
        res.raise_for_status()
        if wait_for_load or wait_for_assurance:
            if not self._check_load_status(ipf, ts, wait_for_assurance, timeout, retry):
                return False
        self._refresh_status(ipf)
        return True

    def _refresh_status(self, ipf: IPFClient):
        results = ipf.fetch(
            "tables/management/snapshots",
            columns=["status", "finishStatus", "loading"],
            filters={"id": ["eq", self.snapshot_id]},
            snapshot=False,
        )[0]
        self.status, self.finish_status, self.loading = (
            results["status"],
            results["finishStatus"],
            results["loading"],
        )

    def _check_load_status(
        self,
        ipf: IPFClient,
        ts: int,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ):
        job = Jobs(client=ipf)
        load_job = job.check_snapshot_load_job(self.snapshot_id, started=ts, timeout=timeout, retry=retry)
        if load_job:
            ae_settings = self.get_assurance_engine_settings(ipf)
            if wait_for_assurance and ae_settings:
                ae_status = job.check_snapshot_assurance_jobs(
                    self.snapshot_id, ae_settings, started=load_job["startedAt"], timeout=timeout, retry=retry
                )
                if not ae_status:
                    logger.error("Assurance Engine tasks did not complete")
                    return False
            elif wait_for_assurance and not ae_settings:
                logger.error("Could not get Assurance Engine tasks please check permissions.")
                return False
        else:
            logger.error("Snapshot Load did not complete.")
            return False
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
        if not path.name.endswith(".tar"):
            path = Path(f"{path.name}.tar")

        # start download job
        ts = int(datetime.now().timestamp() * 1000)
        resp = ipf.get(f"/snapshots/{self.snapshot_id}/download")
        resp.raise_for_status()
        jobs = Jobs(client=ipf)

        # waiting for download job to process
        job = jobs.get_snapshot_download_job(self.snapshot_id, started=ts, retry=retry, timeout=timeout)
        if job:
            filename = ipf.get(f"jobs/{job['id']}/download")
            with open(path, "wb") as fp:
                fp.write(filename.read())
            return path
        logger.error(f"Download job did not finish within {retry * timeout} seconds, could not get file.")
        return None

    def get_snapshot_settings(self, ipf: Union[IPFClient, IPFabricAPI]):
        res = ipf.get(f"/snapshots/{self.snapshot_id}/settings")
        try:
            res.raise_for_status()
            return res.json()
        except HTTPError:
            logger.warning(
                "User/Token does not have access to `snapshots/:key/settings`; "
                "cannot get status of Assurance Engine tasks."
            )
        return None

    def get_assurance_engine_settings(self, ipf: Union[IPFClient, IPFabricAPI]):
        settings = self.get_snapshot_settings(ipf)
        if settings is None:
            logger.error(f"Could not get Snapshot {self.snapshot_id} Settings to verify Assurance Engine tasks.")
            return None
        disabled = settings.get("disabledPostDiscoveryActions", list())
        self.disabled_graph_cache = True if "graphCache" in disabled else False
        self.disabled_historical_data = True if "historicalData" in disabled else False
        self.disabled_intent_verification = True if "intentVerification" in disabled else False
        return dict(
            disabled_graph_cache=self.disabled_graph_cache,
            disabled_historical_data=self.disabled_historical_data,
            disabled_intent_verification=self.disabled_intent_verification,
        )

    def update_assurance_engine_settings(
        self,
        ipf: Union[IPFClient, IPFabricAPI],
        disabled_graph_cache: bool = False,
        disabled_historical_data: bool = False,
        disabled_intent_verification: bool = False,
        wait_for_assurance: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ):
        settings = self.get_snapshot_settings(ipf)
        if settings is None:
            logger.error(
                f"Could not get Snapshot {self.snapshot_id} Settings and cannot update Assurance Engine tasks."
            )
            return False
        current = set(settings.get("disabledPostDiscoveryActions", list()))
        disabled, ae_settings = self._calculate_new_ae_settings(
            current, disabled_graph_cache, disabled_historical_data, disabled_intent_verification
        )
        if disabled == current:
            logger.info("No changes to Assurance Engine Settings required.")
            return True
        ts = int(datetime.now().timestamp() * 1000)
        res = ipf.patch(
            f"/snapshots/{self.snapshot_id}/settings", json=dict(disabledPostDiscoveryActions=list(disabled))
        )
        res.raise_for_status()
        if wait_for_assurance and current - disabled:
            job = Jobs(client=ipf)
            ae_status = job.check_snapshot_assurance_jobs(
                self.snapshot_id, ae_settings, started=ts, timeout=timeout, retry=retry
            )
            if not ae_status:
                logger.error("Assurance Engine tasks did not complete")
                return False
        return True

    @staticmethod
    def _calculate_new_ae_settings(
        current: set,
        disabled_graph_cache: bool = False,
        disabled_historical_data: bool = False,
        disabled_intent_verification: bool = False,
    ):
        disabled = set()
        if disabled_graph_cache:
            disabled.add("graphCache")
        if disabled_historical_data:
            disabled.add("historicalData")
        if disabled_intent_verification:
            disabled.add("intentVerification")
        enabled = current - disabled

        ae_settings = dict(
            disabled_graph_cache=False if "graphCache" in enabled else True,
            disabled_historical_data=False if "historicalData" in enabled else True,
            disabled_intent_verification=False if "intentVerification" in enabled else True,
        )

        return disabled, ae_settings
