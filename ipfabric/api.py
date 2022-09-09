import logging
from collections import OrderedDict

try:
    from importlib import metadata
except ImportError:
    from pkg_resources import get_distribution
from typing import Optional
from urllib.parse import urljoin

from httpx import Client
from ipfabric_httpx_auth import PasswordCredentials, HeaderApiKey
from packaging.version import parse
from pydantic import BaseSettings

from ipfabric import models
from ipfabric.settings.user_mgmt import User

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
        super().__init__(timeout=kwargs.get("timeout", True), headers={"Content-Type": "application/json"})
        with Settings() as settings:
            self.verify = kwargs.get("verify") if "verify" in kwargs else settings.ipf_verify
            base_url = base_url or settings.ipf_url
            if not base_url and not settings.ipf_url:
                raise RuntimeError("IP Fabric base_url not provided or IPF_URL not set")

            self.api_version, self.os_version = self.check_version(api_version or settings.ipf_version, base_url)
            self.base_url = (
                urljoin(base_url, f"api/{self.api_version}/")
                if not settings.ipf_dev
                else urljoin(base_url, f"{self.api_version}/")
            )  # TODO: Verify 5.0 Dev Image stuff
            token = token or settings.ipf_token
            username = username or settings.ipf_username
            password = password or settings.ipf_password

        if not token and not (username and password):
            raise RuntimeError("IP Fabric Token or Username/Password not provided.")

        self.auth = (
            HeaderApiKey(token) if token else PasswordCredentials(base_url, username, password, self.api_version)
        )
        # Get Current User, by doing that we are also ensuring the token is valid
        self.user = self.get_user()
        self.snapshots = self.get_snapshots()
        self.snapshot_id = snapshot_id

    def get_user(self):
        """
        Gets current logged in user information.
        :return: User: User model of logged in user
        """
        resp = self.get("users/me")
        resp.raise_for_status()
        return User(**resp.json())

    def check_version(self, api_version, base_url):
        """
        Checks API Version and returns the version to use in the URL and the OS Version
        :param api_version: str: User defined API Version or None
        :param base_url: str: URL of IP Fabric
        :return: api_version, os_version
        """
        if api_version == "v1":
            raise RuntimeError("IP Fabric Version < 5.0 support has been dropped, please use ipfabric==4.4.3")
        try:
            dist_ver = metadata.version("ipfabric").split(".")
        except NameError:
            dist_ver = get_distribution("ipfabric").version.split(".")
        api_version = parse(api_version) if api_version else parse(f"{dist_ver[0]}.{dist_ver[1]}")

        resp = self.get(urljoin(base_url, "api/version"), headers={"Content-Type": "application/json"})
        resp.raise_for_status()
        os_api_version = parse(resp.json()["apiVersion"])
        if api_version > os_api_version:
            logger.warning(
                f"Specified API or SDK Version ({api_version}) is greater then "
                f"OS API Version.\nUsing OS Version:  ({os_api_version})"
            )
            api_version = os_api_version
        elif os_api_version.major > api_version.major:
            raise RuntimeError(
                f"OS Major Version {os_api_version.major} is greater then SDK Version "
                f"{api_version.major}.  Please upgrade the Python SDK to the new major version."
            )

        return f"v{api_version.major}.{api_version.minor}", parse(resp.json()["releaseVersion"])

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
            raise ValueError(f"##ERROR## EXIT -> Incorrect Snapshot ID: '{snapshot_id}'")
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
