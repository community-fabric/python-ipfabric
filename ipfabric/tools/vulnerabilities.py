from typing import Optional

from pydantic import BaseModel

from ipfabric.tools.nist import NIST, CVEs


class Version(BaseModel):
    vendor: str
    family: Optional[str]
    version: str
    cves: CVEs
    hostname: Optional[str]
    site: Optional[str]


class Vulnerabilities:
    def __init__(self, ipf, timeout: int = 30, cve_limit: int = 20):
        self.ipf = ipf
        self.nist = NIST(timeout=timeout, cve_limit=cve_limit)

    def __del__(self):
        try:
            self.nist.close()
        except AttributeError:
            pass

    def _check_versions(self, versions):
        cves = list()
        for v in versions:
            cve = self.nist.check_cve(v["vendor"], v["family"], v["version"])
            version = Version(vendor=v["vendor"], family=v["family"], version=v["version"], cves=cve)
            if "hostname" in v:
                version.hostname = v["hostname"]
                version.site = v["siteName"]
            cves.append(version)
        return cves

    def check_versions(self, vendor=None):
        filters = {"vendor": ["like", vendor]} if vendor else None
        versions = self.ipf.fetch_all(
            "tables/management/osver-consistency",
            columns=["vendor", "family", "version"],
            filters=filters,
        )
        return self._check_versions(versions)

    def check_device(self, device):
        devices = self.ipf.inventory.devices.all(
            columns=["hostname", "siteName", "vendor", "family", "version"],
            filters={"hostname": ["like", device]},
        )
        return self._check_versions(devices)

    def check_site(self, site):
        sites = self.ipf.inventory.devices.all(
            columns=["hostname", "siteName", "vendor", "family", "version"],
            filters={"siteName": ["like", site]},
        )
        return self._check_versions(sites)
