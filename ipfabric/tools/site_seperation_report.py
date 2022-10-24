import logging
from copy import deepcopy
from typing import Optional

from pydantic.dataclasses import dataclass

from ipfabric.settings import Attributes, SiteSeparation

logger = logging.getLogger("python-ipfabric")


@dataclass
class Matches:
    hostname: str
    sn: str
    old_site_name: str
    new_site_name: Optional[str]
    rule_type: str
    rule_number: Optional[int]
    rule_note: Optional[str]
    regex: Optional[str]
    transformation: Optional[str]


def check_attributes(ipf, devices):
    matches = list()
    attributes = {a["sn"]: a for a in Attributes(ipf).all(filters={"name": ["eq", "siteName"]})}
    for sn, dev in deepcopy(devices).items():
        if sn in attributes:
            matches.append(Matches(dev["hostname"], sn, attributes[sn]["value"], "attributes", -1, None, None, None))
            devices.pop(sn)
    return matches


def map_devices_to_rules(ipf, snapshot_id: str = "$last"):
    ss = SiteSeparation(ipf)
    devices = {
        d["sn"]: d for d in ipf.inventory.devices.all(columns=["hostname", "sn", "siteName"], snapshot_id=snapshot_id)
    }
    rules = ss.get_separation_rules()

    matches = check_attributes(ipf, devices) if rules["manualEnabled"] else list()

    for idx, rule in enumerate(rules["rules"]):
        data = ss.get_rule_matches(rule)
        for match in data["matched"]:
            if match["sn"] in devices:
                site = match["siteName"] if data["matchingGroupApplied"] else rule["siteName"]
                transformation = rule["transformation"] if rule["transformation"] != "none" else None
                matches.append(
                    Matches(
                        match["hostname"],
                        devices[match["sn"]]["siteName"],
                        match["sn"],
                        site,
                        rule["type"],
                        idx,
                        rule["note"],
                        rule["regex"],
                        transformation,
                    )
                )
                devices.pop(match["sn"], None)

    for sn, dev in devices.items():
        matches.append(Matches(dev["hostname"], sn, dev["siteName"], None, "noMatchingRule", None, None, None, None))
    return [m.__dict__ for m in matches]
