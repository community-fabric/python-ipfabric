import logging
from collections import OrderedDict

import httpx

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata
from typing import Optional, Union, Dict, List, Generator, Any
from urllib.parse import urljoin
from httpx import Client
from http.cookiejar import CookieJar
from pydantic import BaseSettings
import dotenv

from ipfabric import snapshot_models
from ipfabric.settings.user_mgmt import User
from uuid import UUID

logger = logging.getLogger("ipfabric")

LAST_ID, PREV_ID, LASTLOCKED_ID = "$last", "$prev", "$lastLocked"


class AccessToken(httpx.Auth):
    def __init__(self, client: httpx.Client):
        self.client = client

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        response = yield request

        if response.status_code == 401:
            response.read()
            if 'API_EXPIRED_ACCESS_TOKEN' in response.text:
                resp = self.client.post("/api/auth/token")  # Use refreshToken in Cookies to get new accessToken
                resp.raise_for_status()  # Response updates accessToken in shared CookieJar
                request.headers['Cookie'] = 'accessToken=' + self.client.cookies['accessToken']  # Update request
                yield request
        return response


class Settings(BaseSettings):
    ipf_url: str = ""
    ipf_version: str = ""
    ipf_token: str = ""
    ipf_verify: Union[bool, str] = True
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
        auth: Any = None,
        snapshot_id: Optional[str] = LAST_ID,
        unloaded: bool = False,
        **kwargs: Optional[dict],
    ):
        """Initializes the IP Fabric Client

        Args:
            base_url: IP Fabric instance provided in 'base_url' parameter, or the 'IPF_URL' environment variable
            api_version: [Optional] Version of IP Fabric API
            auth: API token, tuple (username, password), or custom Auth to pass to httpx
            snapshot_id: IP Fabric snapshot ID to use by default for database actions - defaults to '$last'
            unloaded: True to load metadata from unloaded snapshots
            **kwargs: Keyword args to pass to httpx
        """
        if kwargs.get("token", None) or kwargs.get("username", None) or kwargs.get("password", None):
            logger.warning(
                "Use of `token='<TOKEN>'` or `username='<USER>', password='<PASS>'` authentication will be deprecated "
                "in v7.0.X, please use `auth='<TOKEN>'` or `auth=('<USER>','<PASS>')` instead.\n"
                "This does not apply to .env file or environment variables (IPF_TOKEN, IPF_USERNAME, IPF_PASSWORD).\n"
                "This is to support custom authentication methods that will be passed directly to HTTPX."
            )
        self.unloaded = unloaded
        # find env file
        dotenv.load_dotenv(dotenv.find_dotenv())
        with Settings() as settings:
            cookie_jar = CookieJar()
            super().__init__(
                timeout=kwargs.get("timeout", True),
                verify=kwargs.get("verify", settings.ipf_verify),
                cookies=cookie_jar,
                **self._httpx_kwargs(kwargs, self.verify)
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
            token = kwargs.get("token", settings.ipf_token)  # TODO: Update this in v7.0
            username = kwargs.get("username", settings.ipf_username)
            password = kwargs.get("password", settings.ipf_password)

        if token:
            self._login(token)
        elif username and password:
            self._login((username, password), base_url=base_url, cookie_jar=cookie_jar)
        else:
            self._login(auth, base_url=base_url, cookie_jar=cookie_jar)  # TODO: Keep only this in v7.0

        # Get Current User, by doing that we are also ensuring the token is valid
        self.user = self.get_user()
        self.snapshots = self.get_snapshots()
        self._attribute_filters = None
        self.snapshot_id = snapshot_id
        logger.debug(
            f"Successfully connected to '{self.base_url.host}' IPF version '{self.os_version}' "
            f"as user '{self.user.username}'"
        )

    @staticmethod
    def _httpx_kwargs(kwargs: dict, verify: bool):
        httpx_kwargs = kwargs.copy()
        remove = ['base_url', 'api_version', 'snapshot_id', 'auth', 'unloaded', 'cookies',
                  'token', 'username', 'password']  # TODO: Remove 'token', 'username', 'password' in v7.0
        [httpx_kwargs.pop(h, None) for h in remove]
        httpx_kwargs['verify'] = verify
        return httpx_kwargs

    def _login(self, auth: Any, base_url: str = None, cookie_jar: CookieJar = None):
        if not auth:
            raise RuntimeError("IP Fabric Authentication not provided.")
        elif isinstance(auth, str):
            self.headers.update({'X-API-Token': auth})
        elif isinstance(auth, tuple):
            resp = self.post('auth/login', json=dict(username=auth[0], password=auth[1]))
            resp.raise_for_status()
            self.auth = AccessToken(httpx.Client(base_url=base_url, cookies=cookie_jar))
        else:
            self.auth = auth

    @property
    def attribute_filters(self):
        return self._attribute_filters

    @attribute_filters.setter
    def attribute_filters(self, attribute_filters: Union[Dict[str, List[str]], None]):
        if attribute_filters:
            logger.warning(
                f"Setting Global Attribute Filter for all tables/diagrams until explicitly unset to None.\n"
                f"This may cause errors on some tables like in Settings.\n"
                f"Adding an Attribute Filter to any function will overwrite the Global Filter.\n"
                f"Filter: {attribute_filters}"
            )
        self._attribute_filters = attribute_filters

    def get_user(self) -> User:
        """Gets current logged in user information.

        Returns:
            User: User model of logged in user
        """
        resp = self.get("users/me")
        resp.raise_for_status()
        return User(**resp.json())

    def check_version(self, api_version: str = None, base_url: str = None, dev: bool = False) -> tuple:
        """Checks API Version and returns the version to use in the URL and the OS Version

        Args:
            api_version: User defined API Version or None
            base_url: URL of IP Fabric
            dev: Internal Use Only

        Returns:
            api_version, os_version
        """
        api_version = (
            api_version.lstrip("v").split(".")
            if api_version
            else importlib_metadata.version("ipfabric").lstrip("v").split(".")
        )

        resp = self.get(urljoin(base_url, "api/version" if not dev else "version"))
        resp.raise_for_status()
        os_api_version = resp.json()["apiVersion"].lstrip("v").split(".")
        return_version = f"v{api_version[0]}.{api_version[1]}" if len(api_version) > 1 else f"v{api_version[0]}"
        if len(api_version) == 1 and api_version[0] > os_api_version[0]:
            logger.warning(
                f"Specified API or SDK Version (v{api_version[0]}) is greater then "
                f"OS API Version. Using OS Version:  (v{os_api_version[0]})"
            )
            return_version = f"v{os_api_version[0]}"
        elif api_version[0:2] > os_api_version[0:2]:
            logger.warning(
                f"Specified API or SDK Version (v{'.'.join(api_version)}) is greater then "
                f"OS API Version. Using OS Version:  (v{'.'.join(os_api_version)})"
            )
            return_version = f"v{os_api_version[0]}.{os_api_version[1]}"
        elif os_api_version[0] > api_version[0]:
            raise RuntimeError(
                f"OS Major Version v{os_api_version[0]} is greater then SDK Version "
                f"v{api_version[0]}.  Please upgrade the Python SDK to the new major version."
            )

        return return_version, resp.json()["releaseVersion"]

    def update(self):
        """get all snapshots and assigns them to an attribute"""
        self.snapshots = self.get_snapshots()

    @property
    def loaded_snapshots(self) -> dict:
        """get only loaded snapshots"""
        return {k: v for k, v in self.snapshots.items() if v.loaded}

    @property
    def unloaded_snapshots(self):
        if not self.unloaded:
            logger.warning("Unloaded snapshots not initialized. Retrieving unloaded snapshots.")
            self.unloaded = True
            self.update()
        return {k: v for k, v in self.snapshots.items() if not v.loaded}

    @property
    def snapshot_id(self):
        """get snapshot Id"""
        return self._snapshot_id

    @property
    def snapshot(self):
        return self.snapshots[self.snapshot_id]

    @snapshot_id.setter
    def snapshot_id(self, snapshot_id):
        snapshot_id = snapshot_id or LAST_ID
        if not self.loaded_snapshots:
            logger.warning("No Snapshots are currently loaded.  Please load a snapshot before querying any data.")
            self._snapshot_id = None
        elif snapshot_id not in self.snapshots:
            # Verify snapshot ID is valid
            raise ValueError(f"Incorrect Snapshot ID: '{snapshot_id}'")
        else:
            self._snapshot_id = self.snapshots[snapshot_id].snapshot_id

    def get_snapshot(self, snapshot_id: str):
        if snapshot_id in self.snapshots:
            return self.snapshots[snapshot_id]
        else:
            payload = {"columns": snapshot_models.SNAPSHOT_COLUMNS, "filters": {"id": ["eq", snapshot_id]}}
            results = self._ipf_pager("tables/management/snapshots", payload)
            if not results:
                logger.error(f"Snapshot {snapshot_id} not found.")
                return None
            get_results = self._get_snapshots()
            snapshot = self._create_snapshot_model(results[0], get_results)
            if snapshot.loaded:
                snapshot.get_assurance_engine_settings(self)
            return snapshot

    @staticmethod
    def _create_snapshot_model(s, get_results):
        return snapshot_models.Snapshot(
            **s,
            licensedDevCount=get_results[s["id"]].get("licensedDevCount", None),
            errors=get_results[s["id"]].get("errors", None),
            version=get_results[s["id"]]["version"],
            initialVersion=get_results[s["id"]].get("initialVersion", None),
        )

    def get_snapshot_id(self, snapshot: Union[snapshot_models.Snapshot, str]):
        """
        Returns a Snapshot ID for a given input.

        Args:
            snapshot: Snapshot model, name, or ID

        Returns:
            Snapshot ID
        """
        if isinstance(snapshot, snapshot_models.Snapshot):
            return snapshot.snapshot_id
        elif snapshot in [LAST_ID, PREV_ID, LASTLOCKED_ID]:
            return self.snapshots[snapshot].snapshot_id
        try:
            UUID(snapshot, version=4)
            return self.snapshots[snapshot].snapshot_id
        except ValueError:
            for snap in list(self.snapshots.values()):
                if snapshot == snap.name:
                    return snap.snapshot_id
        raise ValueError(f"Could not locate Snapshot ID for {snapshot}.")

    def _get_snapshots(self):
        """
        Need to do a GET and POST to get all Snapshot data. See NIM-7223
        POST Missing:
        licensedDevCount
        errors
        version
        initialVersion
        """
        res = self.get("/snapshots")
        res.raise_for_status()
        return {s["id"]: s for s in res.json()}

    def _get_snapshot_settings(self, snapshot_id):
        ae_tasks = dict(graphCache=None, historicalData=None, intentVerification=None)
        res = self.get(f"/snapshots/{snapshot_id}/settings")
        try:
            res.raise_for_status()
            disabled = res.json().get("disabledPostDiscoveryActions", list())
            [ae_tasks.update({t: True if t in disabled else False}) for t in ae_tasks]
        except httpx.HTTPError:
            logger.warning(
                "User/Token does not have access to `snapshots/:key/settings`; "
                "cannot get status of Assurance Engine tasks."
            )
        return ae_tasks

    def get_snapshots(self):
        """Gets all snapshots from IP Fabric and returns a dictionary of {ID:   Snapshot_info}

        Returns:
            Dictionary with ID as key and dictionary with info as the value
        """
        payload = {"columns": snapshot_models.SNAPSHOT_COLUMNS, "sort": {"order": "desc", "column": "tsEnd"}}
        if not self.unloaded:
            logger.warning("Retrieving only loaded snapshots. To load all snapshots set `unloaded` to True.")
            payload["filters"] = {"and": [{"status": ["eq", "done"]}, {"finishStatus": ["eq", "done"]}]}
        results = self._ipf_pager("tables/management/snapshots", payload)
        get_results = self._get_snapshots()

        snap_dict = OrderedDict()
        for s in results:
            snap = self._create_snapshot_model(s, get_results)
            snap_dict[snap.snapshot_id] = snap
            if snap.loaded:
                snap.get_assurance_engine_settings(self)
                if LASTLOCKED_ID not in snap_dict and snap.locked:
                    snap_dict[LASTLOCKED_ID] = snap
                if LAST_ID not in snap_dict:
                    snap_dict[LAST_ID] = snap
                    continue
                if PREV_ID not in snap_dict:
                    snap_dict[PREV_ID] = snap
        return snap_dict

    def _ipf_pager(
        self,
        url: str,
        payload: dict,
        limit: int = 1000,
        start: int = 0,
    ):
        """
        Loops through and collects all the data from the tables
        :param url: str: Full URL to post to
        :param payload: dict: Data to submit to IP Fabric
        :param start: int: Where to start for the data
        :return: list: List of dictionaries
        """
        payload["pagination"] = dict(limit=limit)
        data = list()

        def page(s):
            payload["pagination"]["start"] = s
            r = self.post(url, json=payload)
            r.raise_for_status()
            return r.json()["data"]

        r_data = page(start)
        data.extend(r_data)
        while limit == len(r_data):
            start = start + limit
            r_data = page(start)
            data.extend(r_data)
        return data
