import logging
import re
from json import loads
from typing import Optional, Union, Dict, List
from urllib.parse import urlparse

from ipfabric.api import IPFabricAPI
from ipfabric.intent import Intent
from ipfabric.models import Technology, Inventory, Jobs

logger = logging.getLogger("ipfabric")

DEFAULT_ID = "$last"


def check_format(func):
    """
    Checks to make sure api/v1/ is not in the URL and converts filters from json str to dict
    """

    def wrapper(self, url, *args, **kwargs):
        if "filters" in kwargs and isinstance(kwargs["filters"], str):
            kwargs["filters"] = loads(kwargs["filters"])
        path = urlparse(url or kwargs["url"]).path
        r = re.search(r"^\/?(api/)?v\d(\.\d)?/", path)
        url = path[r.end() :] if r else path
        url = url[1:] if url[0] == "/" else url
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
        unloaded: bool = False,
        **kwargs: Optional[dict],
    ):
        """Initializes the IP Fabric Client

        Args:
            base_url: IP Fabric instance provided in 'base_url' parameter, or the 'IPF_URL' environment variable
            api_version: Version of IP Fabric API
            token: API token or 'IPF_TOKEN' environment variable
            snapshot_id: IP Fabric snapshot ID to use by default for database actions - defaults to '$last'
            username: username to authenticate against IP Fabric
            password: password to authenticate against IP Fabric
            **kwargs: Keyword args to pass to httpx
        """
        super().__init__(base_url, api_version, token, snapshot_id, username, password, unloaded, **kwargs)
        self.inventory = Inventory(client=self)
        self.intent = Intent(client=self)
        self.technology = Technology(client=self)
        self.jobs = Jobs(client=self)

    def _check_payload(self, payload, snapshot, filters, reports, sort, attr_filters):
        if not snapshot:
            payload.pop("snapshot", None)
        if filters:
            payload["filters"] = filters
        if reports:
            payload["reports"] = reports
        if sort:
            payload["sort"] = sort
        if attr_filters or self.attribute_filters:
            payload["attributeFilters"] = attr_filters or self.attribute_filters
        return payload

    @check_format
    def fetch(
        self,
        url,
        columns: Optional[List] = None,
        filters: Optional[Union[dict, str]] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot: bool = True,
    ) -> List:
        """Gets data from IP Fabric for specified endpoint

        Args:
            url: Example tables/vlan/device-summary
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters
            limit: Default to 1,000 rows
            start: Starts at 0
            snapshot_id: Optional snapshot_id to override default
            reports: String of frontend URL where the reports are displayed
            sort: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            attr_filters: Optional dictionary to apply an Attribute filter
            snapshot: Set to False for some tables like management endpoints.

        Returns:
            list: List of Dictionary objects.
        """
        payload = dict(
            columns=columns or self.get_columns(url),
            pagination=dict(start=start, limit=limit),
            snapshot=snapshot_id or self.snapshot_id,
        )
        payload = self._check_payload(payload, snapshot, filters, reports, sort, attr_filters)
        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.json()["data"]

    @check_format
    def fetch_all(
        self,
        url: str,
        columns: Optional[List] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot: bool = True,
    ) -> List:
        """Gets all data from IP Fabric for specified endpoint

        Args:
            url: Example tables/vlan/device-summary
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters
            snapshot_id: Optional snapshot_id to override default
            reports: String of frontend URL where the reports are displayed
            sort: Optional dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            attr_filters: Optional dictionary to apply an Attribute filter
            snapshot: Set to False for some tables like management endpoints.

        Returns:
            list: List of Dictionary objects.
        """
        payload = dict(columns=columns or self.get_columns(url), snapshot=snapshot_id or self.snapshot_id)
        payload = self._check_payload(payload, snapshot, filters, reports, sort, attr_filters)
        return self._ipf_pager(url, payload)

    @check_format
    def query(self, url: str, payload: Union[str, dict], get_all: bool = True) -> list:
        """Submits a query, does no formatting on the parameters.  Use for copy/pasting from the webpage.

        Args:
            url: Example: https://demo1.ipfabric.io/api/v1/tables/vlan/device-summary or tables/vlan/device-summary
            payload: Dictionary to submit in POST or can be JSON string (i.e. read from file).
            get_all: Default use pager to get all results and ignore pagination information in the payload


        Returns:
            list: List of Dictionary objects.
        """
        if isinstance(payload, str):
            payload = loads(payload)
        if get_all:
            return self._ipf_pager(url, payload)
        else:
            res = self.post(url, json=payload)
            res.raise_for_status()
            return res.json()["data"]

    def _get_columns(self, url: str):
        logger.warning("""Use of _get_columns will be deprecated in a future release, please use get_columns""")
        return self.get_columns(url)

    def get_columns(self, url: str):
        """Submits malformed payload and extracts column names from it

        Args:
            url: API url to post

        Returns:
            list: List of column names
        """
        r = self.post(url, json=dict(snapshot=self.snapshot_id, columns=["*"]))
        if r.status_code == 422:
            msg = r.json()["errors"][0]["message"]
            return [x.strip() for x in re.match(r"\".*\".*\[(.*)]$", msg).group(1).split(",")]
        else:
            r.raise_for_status()

    def get_count(
        self,
        url: str,
        filters: Optional[Union[dict, str]] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot_id: Optional[str] = None,
        snapshot: bool = True,
    ) -> int:
        """Get a total number of rows
        Args:
            url: Full URL to post to
            filters: Optional dictionary of filters
            attr_filters: Optional dictionary of attribute filters
            snapshot_id: Optional snapshot_id to override default
            snapshot: Set to False for some tables like management endpoints.
        Returns:
            int: a count of rows
        """
        payload = dict(columns=["id"], pagination=dict(limit=1, start=0), snapshot=snapshot_id or self.snapshot_id)
        payload = self._check_payload(payload, snapshot, filters, None, None, attr_filters)
        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.json()["_meta"]["count"]
