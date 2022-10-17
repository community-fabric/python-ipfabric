from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric import IPFClient

import logging
from typing import Optional, List

from pydantic.dataclasses import dataclass

logger = logging.getLogger("python-ipfabric")


@dataclass
class Attributes:
    client: IPFClient
    snapshot_id: Optional[str]

    @property
    def endpoint(self):
        return "attributes/local" if self.snapshot_id else "attributes/global"

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
            "tables/global-attributes", columns=columns, filters=filters, sort=sort, snapshot=False
        ) if self.snapshot_id else self.client.fetch_all(
            "tables/snapshot-attributes", columns=columns, filters=filters, sort=sort, snapshot_id=self.snapshot_id
        )

    def set_attribute_by_sn(self, serial_number, name, value):
        """
        Set a single site by serial number
        :param serial_number: str: IP Fabric Unique Serial Number
        :param name: str: Attribute name (case sensitive)
        :param value: str: Attribute value (case sensitive)
        :return:
        """
        resp = self.client.post(self.endpoint, json=dict(name=name, sn=serial_number, value=value))
        resp.raise_for_status()
        return resp.json()

    def set_attributes_by_sn(self, sites: List[dict]):
        """
        Sets a list of sites for devices based on serial numbers.
        :param sites: list: [{'sn': 'IPF SERIAL NUMBER', 'value': 'SITE NAME'}]
        :return:
        """
        [a.update(dict(name="siteName")) for a in sites]
        resp = self.client.put(self.endpoint, json=dict(attributes=sites))
        resp.raise_for_status()
        return resp.json()

    def set_site_by_sn(self, serial_number, site_name):
        """
        Set a single site by serial number
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
        resp = self.client.put(self.endpoint, json=dict(attributes=sites))
        resp.raise_for_status()
        return resp.json()

    def delete_attribute_by_sn(self, *serial_numbers):
        """
        Deletes attributes by Unique IP Fabric Serial Number(s)
        :param serial_numbers: str: Serial Numbers
        :return:
        """
        serial_numbers = [str(i) for i in serial_numbers]
        resp = self.client.request("DELETE", self.endpoint, json=dict(attributes=dict(sn=serial_numbers)))
        resp.raise_for_status()
        return True

    def delete_attribute_by_id(self, *attribute_ids):
        """
        Deletes attributes by Attribute ID(s)
        :param attribute_ids: str: Attribute IDs
        :return:
        """
        attribute_ids = [str(i) for i in attribute_ids]
        resp = self.client.request("DELETE", self.endpoint, json=dict(attributes=dict(id=attribute_ids)))
        resp.raise_for_status()
        return True
