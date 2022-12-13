import logging
from time import sleep
from typing import Optional, Any, Dict, List, Union

import deepdiff
from pydantic import BaseModel

from ipfabric.technology import *

logger = logging.getLogger("ipfabric")


class Table(BaseModel):
    endpoint: str
    client: Any
    snapshot: bool = True

    @property
    def name(self):
        return self.endpoint.split("/")[-1]

    def fetch(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
        limit: Optional[int] = 1000,
        start: Optional[int] = 0,
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param attr_filters: dict: Optional dictionary of Attribute filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :param limit: int: Default to 1,000 rows
        :param start: int: Starts at 0
        :return: list: List of Dictionaries
        """
        return self.client.fetch(
            self.endpoint,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            limit=limit,
            start=start,
            snapshot=self.snapshot,
        )

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[str] = None,
        sort: Optional[dict] = None,
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param attr_filters: dict: Optional dictionary of Attribute filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :param reports: str: String of frontend URL where the reports are displayed
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :return: list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.endpoint,
            columns=columns,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            snapshot=self.snapshot,
        )

    def count(
        self,
        filters: Optional[dict] = None,
        snapshot_id: Optional[str] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Gets count of table
        :param filters: dict: Optional filters
        :param attr_filters: dict: Optional dictionary of Attribute filters
        :param snapshot_id: str: Optional snapshot ID to override class
        :return: int: Count
        """
        return self.client.get_count(
            self.endpoint,
            filters=filters,
            attr_filters=attr_filters,
            snapshot_id=snapshot_id,
            snapshot=self.snapshot,
        )

    def _compare_determine_columns(self, table_columns: set, columns: set, columns_ignore: set):
        """
        Determines which columns to use in the query.
        Args:
            table_columns: set : Set of columns in the table
            columns: set : Set of columns to use
            columns_ignore: set : Set of columns to ignore

        Returns:
            list[str]: List of columns to use
        """

        # Must always ignore 'id' column
        columns_ignore.add("id")

        cols_for_return = list()
        # user passes columns
        if columns:
            if not table_columns.issuperset(columns):
                raise ValueError(f"Column(s) {columns - table_columns} not in table {self.name}")
            for col in columns:
                if col in columns_ignore and col != "id":
                    logger.debug(f"Column {col} in columns_ignore, ignoring")
                    continue
                cols_for_return.append(col)
        # user does not pass columns
        else:
            for col in table_columns:
                if col in columns_ignore and col != "id":
                    logger.debug(f"Column {col} in columns_ignore, ignoring")
                    continue
                cols_for_return.append(col)
        return cols_for_return

    @staticmethod
    def _hash_data(json_data):
        """
        Hashes data. Turns any data into a string and hashes it, then returns the hash as a key for the data
        Args:
            json_data: list[dict] : List of dictionaries to hash

        Returns:
            list[dict]: List of dictionaries with hash as key
        """
        # loop over each obj, turn the obj into a string, and hash it
        return_json = dict()
        for dict_obj in json_data:
            return_json[deepdiff.DeepHash(dict_obj)[dict_obj]] = dict_obj
        return return_json

    def compare(
        self,
        snapshot_id: str = None,
        reverse: bool = False,
        columns: Union[list, set] = None,
        columns_ignore: Union[list, set] = None,
        **kwargs,
    ):
        """
        Compares a table from the current snapshot to the snapshot_id passed.
        Args:
            snapshot_id: str : The snapshot_id to compare to.
            reverse: bool : If True, will compare the snapshot_id to the current snapshot.
            columns: list : List of columns to compare. If None, will compare all columns.
            columns_ignore: list : List of columns to ignore. If None, will always ignore 'id' column.
            **kwargs: dict : Optional Table.all() arguments to apply to the table before comparing.

        Returns:
            list : List of dictionaries containing the differences between the two snapshots.
        """

        # get all columns for the table
        table_cols = set(self.client._get_columns(self.endpoint))

        # determine which columns to use in query
        columns = set() if columns is None else set(columns)
        columns_ignore = set() if columns_ignore is None else set(columns_ignore)
        cols_for_query = self._compare_determine_columns(table_cols, columns, columns_ignore)

        if reverse:
            data = self.all(snapshot_id=snapshot_id, columns=cols_for_query, **kwargs)
            data_compare = self.all(columns=cols_for_query, **kwargs)
        else:
            data = self.all(columns=cols_for_query, **kwargs)
            data_compare = self.all(snapshot_id=snapshot_id, columns=cols_for_query, **kwargs)
        hashed_data = self._hash_data(data)
        hashed_data_compare = self._hash_data(data_compare)
        # since we turned the values into a hash, we can just compare the keys
        return [
            hashed_data[hashed_str] for hashed_str in hashed_data.keys() if hashed_str not in hashed_data_compare.keys()
        ]


class Inventory(BaseModel):
    client: Any

    @property
    def sites(self):
        return Table(client=self.client, endpoint="/tables/inventory/sites")

    @property
    def vendors(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/vendors")

    @property
    def devices(self):
        return Table(client=self.client, endpoint="/tables/inventory/devices")

    @property
    def models(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/models")

    @property
    def os_version_consistency(self):
        return Table(client=self.client, endpoint="tables/management/osver-consistency")

    @property
    def eol_summary(self):
        return Table(client=self.client, endpoint="tables/reports/eof/summary")

    @property
    def eol_details(self):
        return Table(client=self.client, endpoint="tables/reports/eof/detail")

    @property
    def platforms(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/platforms")

    @property
    def pn(self):
        return Table(client=self.client, endpoint="/tables/inventory/pn")

    @property
    def families(self):
        return Table(client=self.client, endpoint="/tables/inventory/summary/families")

    @property
    def interfaces(self):
        return Table(client=self.client, endpoint="/tables/inventory/interfaces")

    @property
    def hosts(self):
        return Table(client=self.client, endpoint="tables/addressing/hosts")

    @property
    def phones(self):
        return Table(client=self.client, endpoint="tables/inventory/phones")

    @property
    def fans(self):
        return Table(client=self.client, endpoint="tables/inventory/fans")

    @property
    def modules(self):
        return Table(client=self.client, endpoint="tables/inventory/modules")


class Technology(BaseModel):
    client: Any

    @property
    def platforms(self):
        return Platforms(client=self.client)

    @property
    def interfaces(self):
        return Interfaces(client=self.client)

    @property
    def neighbors(self):
        return Neighbors(client=self.client)

    @property
    def dhcp(self):
        return Dhcp(client=self.client)

    @property
    def port_channels(self):
        return PortChannels(client=self.client)

    @property
    def vlans(self):
        return Vlans(client=self.client)

    @property
    def stp(self):
        return Stp(client=self.client)

    @property
    def addressing(self):
        return Addressing(client=self.client)

    @property
    def fhrp(self):
        return Fhrp(client=self.client)

    @property
    def managed_networks(self):
        return ManagedNetworks(client=self.client)

    @property
    def mpls(self):
        return Mpls(client=self.client)

    @property
    def multicast(self):
        return Multicast(client=self.client)

    @property
    def cloud(self):
        return Cloud(client=self.client)

    @property
    def management(self):
        return Management(client=self.client)

    @property
    def ip_telephony(self):
        return IpTelephony(client=self.client)

    @property
    def load_balancing(self):
        return LoadBalancing(client=self.client)

    @property
    def oam(self):
        return Oam(client=self.client)

    @property
    def qos(self):
        return Qos(client=self.client)

    @property
    def routing(self):
        return Routing(client=self.client)

    @property
    def sdn(self):
        return Sdn(client=self.client)

    @property
    def sdwan(self):
        return Sdwan(client=self.client)

    @property
    def security(self):
        return Security(client=self.client)

    @property
    def wireless(self):
        return Wireless(client=self.client)


class Jobs(BaseModel):
    client: Any

    @property
    def all_jobs(self):
        return Table(client=self.client, endpoint="tables/jobs", snapshot=False)

    @property
    def columns(self):
        return [
            "id",
            "downloadFile",
            "finishedAt",
            "isDone",
            "name",
            "scheduledAt",
            "snapshot",
            "startedAt",
            "status",
            "username",
        ]

    def _return_job_when_done(self, job_filter: dict, retry: int = 5, timeout: int = 5):
        if "name" not in job_filter and "snapshot" not in job_filter:
            raise SyntaxError("Must provide a Snapshot ID and name for a filter.")
        retries = 0
        sleep(2)  # Sleep as 1st request could be wrong
        while retries < retry:
            jobs = self.all_jobs.fetch(
                filters=job_filter, sort={"order": "desc", "column": "startedAt"}, columns=self.columns
            )
            if jobs and jobs[0]["isDone"]:
                return jobs[0]
            logger.info(
                f"{job_filter['name'][1]} job is not ready for snapshot {job_filter['snapshot'][1]} ({retries}/{retry})"
            )
            retries += 1
            sleep(timeout)
        return None

    def get_snapshot_download_job(self, snapshot_id: str, started: int, retry: int = 5, timeout: int = 5):
        """Returns a Job Id to use to in a download snapshot

        Args:
            snapshot_id: UUID of a snapshot
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            job_id: str: id to use when downloading a snapshot
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "snapshotDownload"], startedAt=["gte", started - 100])
        return self._return_job_when_done(j_filter, retry=retry, timeout=timeout)

    def check_snapshot_load_job(self, snapshot_id: str, started: int, retry: int = 5, timeout: int = 5):
        """Checks to see if a snapshot load job is completed.

        Args:
            snapshot_id: UUID of a snapshot
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            Job dictionary if load is completed, None if still loading
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "snapshotLoad"], startedAt=["gte", started - 100])
        return self._return_job_when_done(j_filter, retry=retry, timeout=timeout)

    def check_snapshot_unload_job(self, snapshot_id: str, started: int, retry: int = 5, timeout: int = 5):
        """Checks to see if a snapshot load job is completed.

        Args:
            snapshot_id: UUID of a snapshot
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            Job dictionary if load is completed, None if still loading
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "snapshotUnload"], startedAt=["gte", started - 100])
        return self._return_job_when_done(j_filter, retry=retry, timeout=timeout)

    def check_snapshot_assurance_jobs(
        self, snapshot_id: str, assurance_settings: dict, started: int, retry: int = 5, timeout: int = 5
    ):
        """Checks to see if a snapshot Assurance Engine calculation jobs are completed.

        Args:
            snapshot_id: UUID of a snapshot
            assurance_settings: Dictionary from Snapshot.get_assurance_engine_settings
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            True if load is completed, False if still loading
        """
        j_filter = dict(snapshot=["eq", snapshot_id], name=["eq", "loadGraphCache"], startedAt=["gte", started - 100])
        if (
            assurance_settings["disabled_graph_cache"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Graph Cache did not finish loading; Snapshot is not fully loaded yet.")
            return False
        j_filter["name"] = ["eq", "saveHistoricalData"]
        if (
            assurance_settings["disabled_historical_data"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Historical Data did not finish loading; Snapshot is not fully loaded yet.")
            return False
        j_filter["name"] = ["eq", "report"]
        if (
            assurance_settings["disabled_intent_verification"] is False
            and self._return_job_when_done(j_filter, retry=retry, timeout=timeout) is None
        ):
            logger.error("Intent Calculations did not finish loading; Snapshot is not fully loaded yet.")
            return False
        return True
