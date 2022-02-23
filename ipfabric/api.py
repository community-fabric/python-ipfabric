from collections import OrderedDict
from typing import Optional
from urllib.parse import urljoin

from httpx import Client
from pydantic import BaseSettings

from ipfabric import models

DEFAULT_ID = "$last"


class Settings(BaseSettings):
    ipf_url: str = None
    ipf_token: str = None
    ipf_verify: bool = True
    ipf_dev: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class IPFabricAPI(Client):
    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        snapshot_id: str = DEFAULT_ID,
        **kwargs,
    ):
        """
        Initializes the IP Fabric Client
        :param base_url: str: IP Fabric instance provided in 'base_url' parameter, or the 'IPF_URL' environment variable
        :param token: str: API token or 'IPF_TOKEN' environment variable
        :param snapshot_id: str: IP Fabric snapshot ID to use by default for database actions - defaults to '$last'
        :param kwargs: dict: Keyword args to pass to httpx
        """
        with Settings() as settings:
            if settings.ipf_dev:
                kwargs["base_url"] = urljoin(base_url or settings.ipf_url, "v1/")
            else:
                kwargs["base_url"] = urljoin(base_url or settings.ipf_url, "api/v1/")
            kwargs["verify"] = kwargs.get("verify") if "verify" in kwargs else settings.ipf_verify
            token = token or settings.ipf_token

        if not kwargs["base_url"]:
            raise RuntimeError("IP Fabric base_url not provided or IPF_URL not set")
        if not token:
            raise RuntimeError("IP Fabric token not provided or IPF_TOKEN not set")

        super().__init__(**kwargs)
        self.headers.update({"Content-Type": "application/json", "X-API-Token": token})

        # Request IP Fabric for the OS Version, by doing that we are also ensuring the token is valid
        self.os_version = self.fetch_os_version()
        self.snapshots = self.get_snapshots()
        self.snapshot_id = snapshot_id

    def update(self):
        self.os_version = self.fetch_os_version()
        self.snapshots = self.get_snapshots()

    @property
    def snapshot_id(self):
        return self._snapshot_id

    @snapshot_id.setter
    def snapshot_id(self, snapshot_id):
        snapshot_id = DEFAULT_ID if not snapshot_id else snapshot_id
        if snapshot_id not in self.snapshots:
            # Verify snapshot ID is valid
            raise ValueError(f"##ERROR## EXIT -> Incorrect Snapshot ID: '{snapshot_id}'")
        else:
            self._snapshot_id = self.snapshots[snapshot_id].snapshot_id

    def fetch_os_version(self):
        """
        Gets IP Fabric version to ensure token is correct
        :return: str: IP Fabric version
        """
        res = self.get(url="os/version")
        if not res.is_error:
            try:
                return res.json()["version"]
            except KeyError as exc:
                raise ConnectionError(f"Error While getting the OS version, no Version available, message: {exc.args}")
        else:
            raise ConnectionRefusedError("Verify URL and Token are correct.")

    def get_snapshots(self):
        """
        Gets all snapshots from IP Fabric and returns a dictionary of {ID: Snapshot_info}
        :return: dict[str, Snapshot]: Dictionary with ID as key and dictionary with info as the value
        """
        res = self.get("/snapshots")
        res.raise_for_status()

        snap_dict = OrderedDict()
        for s in res.json():
            snap = models.Snapshot(**s)
            snap_dict[snap.snapshot_id] = snap
            if snap.loaded:
                if "$lastLocked" not in snap_dict and snap.locked:
                    snap_dict["$lastLocked"] = snap
                if DEFAULT_ID not in snap_dict:
                    snap_dict[DEFAULT_ID] = snap
                    continue
                if "$prev" not in snap_dict:
                    snap_dict["$prev"] = snap
        return snap_dict
