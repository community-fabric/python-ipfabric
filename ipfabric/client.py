import re
from json import loads
from typing import Optional, Union
from urllib.parse import urlparse

from ipfabric import models
from ipfabric.api import IPFabricAPI
from ipfabric.intent import Intent

DEFAULT_ID = "$last"


def check_format(func):
    """
    Checks to make sure api/v1/ is not in the URL and converts filters from json str to dict
    """

    def wrapper(self, url, *args, **kwargs):
        if "filters" in kwargs and isinstance(kwargs["filters"], str):
            kwargs["filters"] = loads(kwargs["filters"])
        path = urlparse(url or kwargs["url"]).path
        r = re.search(r"(api/)?v\d(\.\d)?", path)
        url = path[r.end() + 1 :] if r else path
        return func(self, url, *args, **kwargs)

    return wrapper


class IPFClient(IPFabricAPI):
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        token: Optional[str] = None,
        snapshot_id: str = DEFAULT_ID,
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
        super().__init__(base_url, api_version, token, snapshot_id, username, password, **kwargs)
        self.inventory = models.Inventory(client=self)
        self.intent = Intent(client=self)

    @check_format
    def fetch(
        self,
        url,
        columns: Optional[list] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        snapshot: bool = True,
    ):
        """
        Gets data from IP Fabric for specified endpoint
        :param url: str: Example tables/vlan/device-summary
        :param columns: list: Optional list of columns to return, None will return all
        :param filters: dict: Optional dictionary of filters
        :param limit: int: Default to 1,000 rows
        :param start: int: Starts at 0
        :param snapshot_id: str: Optional snapshot_id to override default
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :param snapshot: bool: Set to False for some tables like management endpoints.
        :return: list: List of Dictionary objects.
        """

        payload = dict(
            columns=columns or self._get_columns(url),
            pagination=dict(start=start, limit=limit),
        )
        if snapshot:
            payload["snapshot"] = snapshot_id or self.snapshot_id
        if filters:
            payload["filters"] = filters
        if reports:
            payload["reports"] = reports
        if sort:
            payload["sort"] = sort

        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.json()["data"]

    @check_format
    def fetch_all(
        self,
        url: str,
        columns: Optional[list] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        snapshot: bool = True,
    ):
        """
        Gets all data from IP Fabric for specified endpoint
        :param url: str: Example tables/vlan/device-summary
        :param columns: list: Optional list of columns to return, None will return all
        :param filters: dict: Optional dictionary of filters
        :param snapshot_id: str: Optional snapshot_id to override default
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :param snapshot: bool: Set to False for some tables like management endpoints.
        :return: list: List of Dictionary objects.
        """

        payload = dict(columns=columns or self._get_columns(url))
        if snapshot:
            payload["snapshot"] = snapshot_id or self.snapshot_id
        if filters:
            payload["filters"] = filters
        if reports:
            payload["reports"] = reports
        if sort:
            payload["sort"] = sort

        return self._ipf_pager(url, payload)

    @check_format
    def query(self, url: str, payload: Union[str, dict], all: bool = True):
        """
        Submits a query, does no formating on the parameters.  Use for copy/pasting from the webpage.
        :param url: str: Example: https://demo1.ipfabric.io/api/v1/tables/vlan/device-summary
        :param payload: Union[str, dict]: Dictionary to submit in POST or can be JSON string (i.e. read from file).
        :param all: bool: Default use pager to get all results and ignore pagination information in the payload
        :return: list: List of Dictionary objects.
        """
        if isinstance(payload, str):
            payload = loads(payload)
        if all:
            return self._ipf_pager(url, payload)
        else:
            res = self.post(url, json=payload)
            res.raise_for_status()
            return res.json()["data"]

    def _get_columns(self, url: str):
        """
        Submits malformed payload and extracts column names from it
        :param url: str: API url to post
        :return: list: List of column names
        """
        r = self.post(url, json=dict(snapshot=self.snapshot_id, columns=["*"]))
        if r.status_code == 422:
            msg = r.json()["errors"][0]["message"]
            return [x.strip() for x in re.match(r"\".*\".*\[(.*)]$", msg).group(1).split(",")]
        else:
            r.raise_for_status()

    def _ipf_pager(
        self,
        url: str,
        payload: dict,
        data: Optional[Union[list, None]] = None,
        limit: int = 1000,
        start: int = 0,
    ):
        """
        Loops through and collects all the data from the tables
        :param url: str: Full URL to post to
        :param payload: dict: Data to submit to IP Fabric
        :param data: list: List of data to append subsequent calls
        :param start: int: Where to start for the data
        :return: list: List of dictionaries
        """
        data = data or list()

        payload["pagination"] = dict(limit=limit, start=start)
        r = self.post(url, json=payload)
        r.raise_for_status()
        r = r.json()
        data.extend(r["data"])
        if limit + start < r["_meta"]["count"]:
            self._ipf_pager(url, payload, data, limit=limit, start=start + limit)
        return data

    def get_count(self, url: str, snapshot_id: Optional[str] = None):
        payload = dict(columns=["id"], pagination=dict(limit=1, start=0))
        payload["snapshot"] = snapshot_id or self.snapshot_id
        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.json()["_meta"]["count"]
