import logging
from collections import OrderedDict
from typing import Optional
from urllib.parse import urljoin

import pkg_resources
from httpx import Client
from ipfabric_httpx_auth import PasswordCredentials, HeaderApiKey
from pydantic import BaseSettings

from ipfabric import models

logger = logging.getLogger()
DEFAULT_ID = "$last"


class Settings(BaseSettings):
    ipf_url: str = ""
    ipf_version: str = ""
    ipf_token: str = ""
    ipf_verify: bool = True
    ipf_dev: bool = False
    ipf_username: str = ""
    ipf_password: str = ""

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
        api_version: Optional[str] = None,
        token: Optional[str] = None,
        snapshot_id: Optional[str] = DEFAULT_ID,
        username: Optional[str] = None,
        password: Optional[str] = None,
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
            self.api_version = api_version or settings.ipf_version
            if not self.api_version:
                ver = pkg_resources.get_distribution("ipfabric").version.split(".")
                self.api_version = "v" + ver[0] + "." + ver[1]

            base_url = base_url or settings.ipf_url
            if settings.ipf_dev:
                kwargs["base_url"] = urljoin(base_url, f"{self.api_version}/")
            else:
                kwargs["base_url"] = urljoin(base_url, f"api/{self.api_version}/")
            kwargs["verify"] = kwargs.get("verify") if "verify" in kwargs else settings.ipf_verify
            token = token or settings.ipf_token
            username = username or settings.ipf_username
            password = password or settings.ipf_password

        if not kwargs["base_url"]:
            raise RuntimeError("IP Fabric base_url not provided or IPF_URL not set")
        if not token and not (username and password):
            raise RuntimeError("IP Fabric Token or Username/Password not provided.")

        super().__init__(**kwargs)
        self.headers.update({"Content-Type": "application/json"})
        self.auth = HeaderApiKey(token) if token else PasswordCredentials(base_url, username, password)

        # Request IP Fabric for the OS Version, by doing that we are also ensuring the token is valid
        self.os_version = self.fetch_os_version()
        self.snapshots = self.get_snapshots()
        self.snapshot_id = snapshot_id

    def update(self):
        self.os_version = self.fetch_os_version()
        self.snapshots = self.get_snapshots()

    @property
    def loaded_snapshots(self):
        return {k: v for k, v in self.snapshots.items() if v.loaded}

    @property
    def unloaded_snapshots(self):
        return {k: v for k, v in self.snapshots.items() if not v.loaded}

    @property
    def snapshot_id(self):
        return self._snapshot_id

    @snapshot_id.setter
    def snapshot_id(self, snapshot_id):
        snapshot_id = snapshot_id or DEFAULT_ID
        if not self.loaded_snapshots:
            logger.warning("No Snapshots are currently loaded.  Please load a snapshot before querying any data.")
            self._snapshot_id = None
        elif snapshot_id not in self.snapshots:
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
                return pkg_resources.parse_version(res.json()["version"])
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
