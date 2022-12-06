import logging
import re
from typing import Optional, List, Any

from pydantic import Field
from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")

ATTR_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]+$")


@dataclass
class Attributes:
    """
    Class to retrieve Global and Local (Snapshot specific) Attributes.  You must specify snapshot_id to use local.
    """

    client: Any = Field(description="IPFClient")
    snapshot_id: Optional[str] = Field(default=None, description="Snapshot ID to switch to Local Attributes")

    def __post_init__(self):
        if isinstance(self.snapshot_id, str):
            self.snapshot_id = self.client.get_snapshot(self.snapshot_id).snapshot_id

    @property
    def endpoint(self):
        return "attributes/local" if self.snapshot_id else "attributes/global"

    @property
    def post_endpoint(self):
        return "tables/snapshot-attributes" if self.snapshot_id else "tables/global-attributes"

    @staticmethod
    def check_attribute_name(attributes: set):
        invalid = list()
        for attribute in attributes:
            if not ATTR_REGEX.match(attribute):
                invalid.append(attribute)
        if invalid:
            raise NameError(
                f"The following Attribute Names are invalid and do match regex rule "
                f'"^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]+$":\n{invalid}'
            )
        return True

    def all(
        self,
        columns: list = None,
        filters: Optional[dict] = None,
        sort: Optional[dict] = None,
    ):
        """
        Gets all data from corresponding endpoint
        :param columns: list: Optional columns to return, default is all
        :param filters: dict: Optional filters
        :param sort: dict: Dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
        :return: list: List of Dictionaries
        """
        return self.client.fetch_all(
            self.post_endpoint,
            columns=columns,
            filters=filters,
            sort=sort,
            snapshot=True if self.snapshot_id else False,
            snapshot_id=self.snapshot_id,
        )

    def set_attribute_by_sn(self, serial_number, name, value):
        """
        Set a single Attribute by serial number.
        If Global will Error if already set.
        If Local will not error and either Add or Update
        :param serial_number: str: IP Fabric Unique Serial Number
        :param name: str: Attribute name (case sensitive)
        :param value: str: Attribute value (case sensitive)
        :return:
        """
        self.check_attribute_name({name})
        attribute = dict(name=name, sn=serial_number, value=value)
        if self.snapshot_id:
            return self.set_attributes_by_sn([attribute])
        resp = self.client.post(self.endpoint, json=attribute)
        resp.raise_for_status()
        return resp.json()

    def set_attributes_by_sn(self, attributes: List[dict]):
        """
        Sets a list of Attributes for devices based on serial numbers.
        Will Add or Update Attributes.
        :param attributes: list: [{'sn': 'IPF SERIAL NUMBER', 'name': 'attributeName', 'value': 'SITE NAME'}]
        :return:
        """
        self.check_attribute_name({v["name"] for v in attributes})
        payload = dict(attributes=attributes)
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        resp = self.client.put(self.endpoint, json=payload)
        resp.raise_for_status()
        return resp.json()

    def set_site_by_sn(self, serial_number, site_name):
        """
        Set a single site by serial number
        If Global will Error if already set.
        If Local will not error and either Add or Update
        :param serial_number: str: IP Fabric Unique Serial Number
        :param site_name: str: Site name for device.
        :return:
        """
        return self.set_attribute_by_sn(serial_number, "siteName", site_name)

    def set_sites_by_sn(self, sites: List[dict]):
        """
        Sets a list of sites for devices based on serial numbers.
        :param sites: list: [{'sn': 'IPF SERIAL NUMBER', 'value': 'SITE NAME'}]
        :return:
        """
        [a.update(dict(name="siteName")) for a in sites]
        return self.set_attributes_by_sn(sites)

    def delete_attribute_by_sn(self, *serial_numbers):
        """
        Deletes Attributes by Unique IP Fabric Serial Number(s)
        :param serial_numbers: str: Serial Numbers
        :return:
        """
        payload = dict(attributes=dict(sn=[str(i) for i in serial_numbers]))
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        resp = self.client.request("DELETE", self.endpoint, json=payload)
        resp.raise_for_status()
        return True

    def delete_attribute_by_id(self, *attribute_ids):
        """
        Deletes Attributes by Attribute ID(s)
        :param attribute_ids: str: Attribute IDs
        :return:
        """
        payload = dict(attributes=dict(id=[str(i) for i in attribute_ids]))
        if self.snapshot_id:
            payload["snapshot"] = self.snapshot_id
        resp = self.client.request("DELETE", self.endpoint, json=payload)
        resp.raise_for_status()
        return True

    def delete_attribute(self, *attributes):
        """
        Deletes attributes by Attribute
        :param attributes: dict: Attribute dictionaries
        :return:
        """
        return self.delete_attribute_by_id(*[str(i["id"]) for i in attributes])

    def update_local_attr_from_global(self):
        if not self.snapshot_id:
            raise ImportError(f"Please initialize Attributes class with a snapshot_id.")
        g_attrs = self.client.fetch_all("tables/global-attributes", columns=["name", "value", "sn"], snapshot=False)
        if not g_attrs:
            return False
        local_attrs = self.all()
        if local_attrs:
            self.delete_attribute(*local_attrs)
        self.set_attributes_by_sn(g_attrs)
        return True
