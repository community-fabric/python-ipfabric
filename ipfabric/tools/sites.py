import csv
import logging
from os.path import exists
from typing import Union, Any

from pydantic import Field
from pydantic.dataclasses import dataclass

logger = logging.getLogger()


@dataclass
class UpdateSiteNames:
    ipf: Any
    sites: Union[str, list] = Field(description="List of tuples [(oldName, newName)] or CSV filename to import.")
    dry_run: bool = False

    def __post_init__(self):
        if isinstance(self.sites, str) and exists(self.sites):
            with open(self.sites, "r") as f:
                self.sites = list(csv.reader(f, delimiter=","))
        elif not isinstance(self.sites, list) and not (isinstance(self.sites, str) and exists(self.sites)):
            raise SyntaxError("Sites is not a list of tuples or a filename.")

    def _patch_site(self, key, old, new):
        if self.dry_run:
            return True
        res = self.ipf.patch("sites/" + key, json=dict(name=new))
        if res.status_code == 200:
            logger.warning(f"Changed {old} to {new}")
            return True
        else:
            logger.error(f"Failed to change {old} to {new}")
            return False

    def update_sites(self):
        """
        Applies updates to IP Fabric
        :return: dict: {updated: [oldName, newName], errors: [oldName, newName]}
        """
        ipf_sites = self.ipf.inventory.sites.all(columns=["siteName", "siteKey", "siteUid"])
        names = {s["siteName"]: s for s in ipf_sites}
        uid = {s["siteUid"]: s for s in ipf_sites}
        updates = dict(updated=list(), errors=list())
        for site in self.sites:
            old, new = site[0].strip(), site[1].strip()
            changed = False
            if old in names and names[old]["siteName"] != new:
                changed = self._patch_site(names[old]["siteKey"], old, new)
            elif old in uid and uid[old]["siteName"] != site[1]:
                changed = self._patch_site(uid[old]["siteKey"], uid[old]["siteName"], new)
            elif (old in names and names[old]["siteName"] == new) or (old in uid and uid[old]["siteName"] == new):
                logger.info(f"{old} is already set to {new}")
            else:
                logger.error(f"Could not find {old}")
            if changed:
                updates["updated"].append((old, new))
            else:
                updates["errors"].append((old, new))
        return updates
