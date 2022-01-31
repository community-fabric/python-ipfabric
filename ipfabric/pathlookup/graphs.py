import ipaddress
from typing import Optional, Union


class IPFPath:
    def __init__(self, client):
        self.client = client
        self._style = "json"

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        style = style or "json"
        if style not in ["json", "svg", "png"]:
            raise ValueError(f"##ERROR## EXIT -> Graph style '{style}' must be one of ['json', 'svg', 'png']")
        self._style = style

    def _query(self, payload: dict):
        """
        Submits a query, does no formating on the parameters.  Use for copy/pasting from the webpage.
        :param payload: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = "graphs"
        if self.style == "svg":
            url = "graphs/svg"
        elif self.style == "png":
            url = "graphs/png"
        res = self.client.post(url, json=payload)
        res.raise_for_status()
        if self.style == "json":
            return res.json()
        else:
            return res.content

    def site(
        self,
        site_name: Union[str, list],
        snapshot_id: Optional[str] = None,
        overlay: dict = None,
    ):
        """
        Returns a diagram for a site or sites
        :param site_name: Union[str, list]: A single site name or a list of site names
        :param snapshot_id: str: Optional Snapshot ID
        :param overlay: dict: Optional Overlay dictionary
        :return:
        """
        payload = {
            "parameters": {
                "groupBy": "siteName",
                "layouts": [],
                "paths": [site_name] if isinstance(site_name, str) else site_name,
                "type": "topology",
            },
            "snapshot": snapshot_id or self.client.snapshot_id,
        }
        if overlay:
            payload["overlay"] = overlay
        return self._query(payload)

    def host_to_gw(
        self,
        src_ip: str,
        grouping: Optional[str] = "siteName",
        snapshot_id: Optional[str] = None,
    ) -> Union[dict, bytes]:
        """
        Execute an "Host to Gateway" diagram query for the given set of parameters.
        :param src_ip: str: Source IP address or subnet
        :param grouping: str: Group by "siteName", "routingDomain", "stpDomain"
        :param snapshot_id: str: Snapshot ID to override class default
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        self.check_subnets(src_ip)
        payload = dict(
            parameters=dict(
                startingPoint=src_ip,
                type="pathLookup",
                pathLookupType="hostToDefaultGW",
                groupBy=grouping,
            ),
            snapshot=snapshot_id or self.client.snapshot_id,
        )
        return self._query(payload)

    @staticmethod
    def check_subnets(*ips) -> bool:
        """
        Checks for valid IP Addresses or Subnet
        :param ips: ip addresses
        :return: True if a subnet is found to set to networkMode, False if only hosts
        """
        masks = set()
        for ip in ips:
            try:
                masks.add(ipaddress.IPv4Interface(ip).network.prefixlen)
            except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
                raise ipaddress.AddressValueError(f"{ip} is not a valid IP or subnet.")

        return True if masks != {32} else False
