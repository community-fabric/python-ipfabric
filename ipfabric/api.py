import logging
from collections import OrderedDict

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata
from typing import Optional
from urllib.parse import urljoin

from httpx import Client
from ipfabric_httpx_auth import PasswordCredentials, HeaderApiKey
from pydantic import BaseSettings

from ipfabric import models
from ipfabric.settings.user_mgmt import User


logger = logging.getLogger("ipfabric")

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
        """Needed for context"""
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
            super().__init__(
                timeout=kwargs.get("timeout", True),
                headers={"Content-Type": "application/json"},
                verify=kwargs.get("verify", settings.ipf_verify),
            )
            base_url = base_url or settings.ipf_url
            if not base_url:
                raise RuntimeError("IP Fabric base_url not provided or IPF_URL not set")

            self.api_version, self.os_version = self.check_version(
                api_version or settings.ipf_version, base_url, settings.ipf_dev
            )
            self.base_url = (
                urljoin(base_url, f"api/{self.api_version}/")
                if not settings.ipf_dev
                else urljoin(base_url, f"{self.api_version}/")
            )
            token = token or settings.ipf_token
            username = username or settings.ipf_username
            password = password or settings.ipf_password

        if not token and not (username and password):
            logger.error("IP Fabric Token or Username/Password not provided.")
            raise RuntimeError("IP Fabric Token or Username/Password not provided.")

        self.auth = (
            HeaderApiKey(token) if token else PasswordCredentials(base_url, username, password, self.api_version)
        )
        # Get Current User, by doing that we are also ensuring the token is valid
        self.user = self.get_user()
        self.snapshots = self.get_snapshots()
        self.snapshot_id = snapshot_id
        logger.debug(
            f"Successfully connected to '{self.base_url.host}' IPF version '{self.os_version}' "
            f"as user '{self.user.username}'"
        )

    def get_user(self):
        """
        Gets current logged in user information.
        :return: User: User model of logged in user
        """
        resp = self.get("users/me")
        resp.raise_for_status()
        return User(**resp.json())

    def check_version(self, api_version, base_url, dev=False):
        """
        Checks API Version and returns the version to use in the URL and the OS Version
        :param api_version: str: User defined API Version or None
        :param base_url: str: URL of IP Fabric
        :return: api_version, os_version
        """
        if api_version == "v1":
            raise RuntimeError("IP Fabric Version < 5.0 support has been dropped, please use ipfabric==4.4.3")
        api_version = (
            api_version.lstrip("v").split(".")
            if api_version
            else importlib_metadata.version("ipfabric").lstrip("v").split(".")
        )

        resp = self.get(urljoin(base_url, "api/version" if not dev else "version"))
        resp.raise_for_status()
        os_api_version = resp.json()["apiVersion"].lstrip("v").split(".")
        if api_version[0:2] > os_api_version[0:2]:
            logger.warning(
                f"Specified API or SDK Version ({'.'.join(api_version)}) is greater then "
                f"OS API Version. Using OS Version:  ({'.'.join(os_api_version)})"
            )
            api_version = os_api_version
        elif os_api_version[0] > api_version[0]:
            raise RuntimeError(
                f"OS Major Version {os_api_version[0]} is greater then SDK Version "
                f"{api_version[0]}.  Please upgrade the Python SDK to the new major version."
            )

        return f"v{api_version[0]}.{api_version[1]}", resp.json()["releaseVersion"]

    def update(self):
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
            logger.exception(f"Incorrect Snapshot ID: '{snapshot_id}'")
            raise ValueError(f"Incorrect Snapshot ID: '{snapshot_id}'")
        else:
            self._snapshot_id = self.snapshots[snapshot_id].snapshot_id

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
