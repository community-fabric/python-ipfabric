from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ipfabric import IPFClient
    from ipfabric.snapshot_models import Snapshot
import logging
from typing import Any
import jsondiff as jd
from pydantic import BaseModel

logger = logging.getLogger("python-ipfabric")

HELP_STR = """
Takes a 'dotted' string representing location of tech table.
Example:
    for arp table, pass the string 'addressing.arp_table'
    >>>ipf.technology.addressing.arp_table
Alternatively, takes a tuple of 2 strings representing location of tech table
Example:
    for arp table, pass a tuple ('addressing', 'arp_table')
"""

TECH_TABLE_METHODS_IGNORE =['__abstractmethods__', '__annotations__', '__class__', '__class_vars__', '__config__',
                          '__custom_root_type__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                          '__exclude_fields__', '__fields__', '__fields_set__', '__format__', '__ge__',
                          '__get_validators__', '__getattribute__', '__getstate__', '__gt__', '__hash__',
                          '__include_fields__', '__init__', '__init_subclass__', '__iter__', '__json_encoder__',
                          '__le__', '__lt__', '__module__', '__ne__', '__new__', '__post_root_validators__',
                          '__pre_root_validators__', '__pretty__', '__private_attributes__', '__reduce__',
                          '__reduce_ex__', '__repr__', '__repr_args__', '__repr_name__', '__repr_str__',
                          '__rich_repr__', '__schema_cache__', '__setattr__', '__setstate__', '__signature__',
                          '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__try_update_forward_refs__',
                          '__validators__', '_abc_impl', '_calculate_keys', '_copy_and_set_values', '_decompose_class',
                          '_enforce_dict_if_root', '_get_value', '_init_private_attributes', '_iter', 'schema_json',
                          'parse_file','parse_obj','parse_raw','from_orm','Config']


class IpfTableDiff(BaseModel):
    client: Any

    def _check_tech_table_attr(self, tech_table: [str, tuple[str,str]]):
        """Takes a 'dotted' string representing location of tech table.
        Example:
            for arp table, pass the string 'addressing.arp_table'
            # >>>ipf.technology.addressing.arp_table
        Alternatively, takes a tuple of 2 strings representing location of tech table
        Example:
            for arp table, pass a tuple ('addressing', 'arp_table')
        Args:
            tech_table: string or tuple representing location of tech table

        Returns:
            IPFClient attribute for location of table data to be used in diff
        """
        valid_tables = [method for method in dir(self.client.technology) if method not in TECH_TABLE_METHODS_IGNORE]
        if isinstance(tech_table, (tuple, str)):
            if isinstance(tech_table, str):
                tech_table = tuple(tech_table.split("."))
            if isinstance(tech_table, tuple) and len(tech_table) != 2:
                logger.error(f"unknown table {tech_table}")
                logger.info(f"valid tables: \n {valid_tables}")
                return None
            first_attr = tech_table[0]
            second_attr = tech_table[1]
            tech_table_instance = getattr(self.client.technology, f"{first_attr}", None)
            if tech_table_instance:
                return_client = getattr(tech_table_instance, f"{second_attr}", None)
                if not return_client:
                    valid_tables = [method for method in dir(return_client) if
                                    method not in TECH_TABLE_METHODS_IGNORE]
                    logger.error(f"unable to determine nested table {tech_table}")
                    logger.info(f"valid tables: \n {valid_tables}")
                return return_client
        else:
            logger.error(f"unable to determine nested table {tech_table}")
            logger.info(f"valid tables: \n {valid_tables}")
            logger.info(f"{HELP_STR}")

    def _check_inv_table_attr(self, inv_table: str):
        if hasattr(self.client.inventory, f"{inv_table}"):
            return getattr(self.client.inventory, f"{inv_table}", None)

    def _get_snapshot_id(self,
                         snapshot: Snapshot = None,
                         snapshot_name: str = None,
                         snapshot_id: str = None,
                         ):
        if snapshot:
            return self.client.snapshots[snapshot.snapshot_id].snapshot_id
        if snapshot_name:
            for snap in list(self.client.snapshots.values()):
                if snapshot_name == snap.name:
                    return snap.snapshot_id
        if snapshot_id:
            return self.client.snapshots[snapshot_id].snapshot_id

    def _determine_support(self,
                           snapshot: Snapshot = None,
                           snapshot_name: str = None,
                           snapshot_id: str = None,
                           snapshot_compare: Snapshot = None,
                           snapshot_name_compare: str = None,
                           snapshot_id_compare: str = None
                           ):
        snap_dict = dict()
        snap_dict["snapshot"] = snapshot
        snap_dict["snapshot_id"] = snapshot_id
        snap_dict["snapshot_name"] = snapshot_name
        snap_id = self._get_snapshot_id(**snap_dict)
        logger.debug(f"snapshot config: \n {snap_dict}")
        if not snap_id:
            logger.error("please provide a snapshot to diff, either a snapshot object, name or id")
            return None
        snap_dict = dict()
        snap_dict["snapshot"] = snapshot_compare
        snap_dict["snapshot_id"] = snapshot_id_compare
        snap_dict["snapshot_name"] = snapshot_name_compare
        logger.debug(f"snapshot_compare config: \n {snap_dict}")
        snap_id_compare = self._get_snapshot_id(**snap_dict)
        if not snap_id_compare:
            logger.error("please provide a snapshot to compare, either a snapshot object, name or id")
            return None
        return snap_id, snap_id_compare

    def diff_table(self,
                inv_table : str = None,
                technology: bool = False,
                technology_table: [str, tuple] = None,
                snapshot: Snapshot = None,
                snapshot_name: str = None,
                snapshot_id: str = None,
                snapshot_compare: Snapshot = None,
                snapshot_name_compare: str = None,
                snapshot_id_compare: str = None
                ):
        if technology:
            table_data = self._check_tech_table_attr(technology_table)
        else:
            table_data = self._check_inv_table_attr(inv_table)
        snap_id, snap_id_compare = self._determine_support(snapshot, snapshot_name, snapshot_id,
                                                        snapshot_compare, snapshot_name_compare, snapshot_id_compare)
        return jd.diff(table_data.all(snapshot_id=snap_id), table_data.all(snapshot_id=snap_id_compare))



