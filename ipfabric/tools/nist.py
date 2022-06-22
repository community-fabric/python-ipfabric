from typing import List

from httpx import Client, ReadTimeout, HTTPStatusError
from pydantic import BaseModel, Field


class CVE(BaseModel):
    cve_id: str
    description: str
    url: str

    def __repr__(self):
        return self.cve_id

    def __hash__(self):
        return hash(self.cve_id)


class CVEs(BaseModel):
    total_results: int
    cves: List[CVE]
    error: str = Field(default=None)


class NIST(Client):
    def __init__(self, timeout, cve_limit):
        super().__init__(base_url="https://services.nvd.nist.gov/rest/json/cves/1.0", timeout=timeout)
        self.cve_limit = cve_limit

    @property
    def params(self):
        return {
            "cpeMatchString": "cpe:2.3:*:",
            "startIndex": 0,
            "resultsPerPage": self.cve_limit,
        }

    def check_cve(self, vendor: str, family: str, version: str):
        """

        :param vendor: str: Vendor for the device to be checked
        :param family: str: Family of the device to be checked
        :param version: str: Software version of the device to be checked
        :return:
        """
        params = self.params
        if vendor in ["azure", "aws"]:
            return CVEs(total_results=0, cves=[], error="Unsupported")
        elif vendor == "juniper":
            version = version[: version.rfind("R") + 2].replace("R", ":r")
            params["cpeMatchString"] += vendor + ":" + family + ":" + version
        elif vendor == "paloalto":
            params["cpeMatchString"] += "palo_alto" + ":" + family + ":" + version
        elif vendor == "extreme":
            if "xos" in family:
                family = "extremexos"
            params["cpeMatchString"] += "extremenetworks" + ":" + family + ":" + version
        elif "aruba" in family:
            params["cpeMatchString"] += "arubanetworks:arubaos" + ":" + version
        elif vendor == "f5" and family == "big-ip":
            params["cpeMatchString"] += vendor + ":" + "big-ip_access_policy_manager" + ":" + version
        elif vendor == "cisco":
            if family == "meraki":
                return CVEs(total_results=0, cves=[], error="Unsupported")
            elif family == "wlc-air":
                family = "wireless_lan_controller_software"
            elif family == "ftd":
                family = "firepower"
                version = (version.replace("(Bu", ".Bu")).replace(")", ".").split(" .", 1)[0]
            elif family != "nx-os":
                family = family.replace("-", "_")
            version = (version.replace("(", ".")).replace(")", ".")
            params["cpeMatchString"] += vendor + ":" + family + ":" + version
        elif vendor == "fortinet" and family == "fortigate":
            params["cpeMatchString"] += "fortinet:fortios:" + version.replace(",", ".")
        elif vendor == "checkpoint" and family == "gaia":
            params["cpeMatchString"] += vendor + ":" + "gaia_os" + version.replace("R", ":r")
        elif vendor == "arista":
            params["cpeMatchString"] += vendor + ":" + family + ":" + version.lower()
        else:
            return CVEs(total_results=0, cves=[], error="Unsupported")

        try:
            res = self.get("", params=params)
            res.raise_for_status()
            data = res.json()

            cves = CVEs(
                total_results=data["totalResults"],
                cves=[
                    CVE(
                        cve_id=i["cve"]["CVE_data_meta"]["ID"],
                        description=i["cve"]["description"]["description_data"][0]["value"],
                        url=i["cve"]["references"]["reference_data"][0]["url"],
                    )
                    for i in data["result"]["CVE_Items"]
                ],
            )
            return cves
        except ReadTimeout:
            return CVEs(total_results=0, cves=[], error="Timeout")
        except HTTPStatusError:
            return CVEs(total_results=0, cves=[], error="HTTP Error")
