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

    def unicast(
            self,
            src_ip: str,
            dst_ip: str,
            proto: str = "tcp",
            src_port: Optional[int] = 10000,
            dst_port: Optional[int] = 80,
            sec_drop: Optional[bool] = True,
            grouping: Optional[str] = "siteName",
            flags: Optional[list] = None,
            snapshot_id: Optional[str] = None
    ) -> Union[dict, bytes]:
        """
        Execute an Unicast Path Lookup diagram query for the given set of parameters.

        :param src_ip: str: Source IP address or subnet
        :param dst_ip: str: Destination IP address/subnet
        :param proto: str: Protocol "tcp", "udp", or "icmp"
        :param src_port: int: Source Port for tcp or udp
        :param dst_port: int: Destination Port for tcp or udp
        :param sec_drop: bool: True specifies Security Rules will Drop packets and not Continue
        :param grouping: str:  Group by "siteName", "routingDomain", "stpDomain"
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        :param snapshot_id: str: Snapshot ID to override class default
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        parameters = dict(
            startingPoint=src_ip,
            startingPort=src_port,
            destinationPoint=dst_ip,
            destinationPort=dst_port,
            protocol=proto,
            type="pathLookup",
            securedPath=sec_drop,
            pathLookupType="unicast",
            groupBy=grouping,
            networkMode=self.check_subnets(src_ip, dst_ip)
        )
        payload = dict(
            parameters=self.check_proto(parameters, flags),
            snapshot=snapshot_id or self.client.snapshot_id
        )

        return self._query(payload)

    def multicast(
            self,
            src_ip: str,
            grp_ip: str,
            proto: str = "tcp",
            rec_ip: Optional[str] = None,
            src_port: Optional[int] = 10000,
            grp_port: Optional[int] = 80,
            sec_drop: Optional[bool] = True,
            grouping: Optional[str] = "siteName",
            flags: Optional[list] = None,
            snapshot_id: Optional[str] = None
    ) -> Union[dict, bytes]:
        """
        Execute an Multicast Path Lookup diagram query for the given set of parameters.

        :param src_ip: str: Source IP address
        :param grp_ip: str: Multicast group IP address
        :param proto: str: Protocol "tcp", "udp", or "icmp"
        :param rec_ip: str: Receiver IP address
        :param src_port: int: Source Port for tcp or udp
        :param grp_port: int: Destination Port for tcp or udp
        :param sec_drop: bool: True specifies Security Rules will Drop packets and not Continue
        :param grouping: str:  Group by "siteName", "routingDomain", "stpDomain"
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        :param snapshot_id: str: Snapshot ID to override class default
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        if self.check_subnets(src_ip, grp_ip):
            raise SyntaxError("Multicast does not support subnets, please provide a single IP for Source and Group")

        parameters = dict(
            source=src_ip,
            sourcePort=src_port,
            group=grp_ip,
            groupPort=grp_port,
            protocol=proto,
            type="pathLookup",
            securedPath=sec_drop,
            pathLookupType="multicast",
            groupBy=grouping
        )
        if rec_ip and self.check_subnets(rec_ip):
            raise SyntaxError("Multicast Receiver IP must be a single IP not subnet.")
        elif rec_ip:
            parameters['receiver'] = rec_ip

        payload = dict(
            parameters=self.check_proto(parameters, flags),
            snapshot=snapshot_id or self.client.snapshot_id
        )

        return self._query(payload)

    def host_to_gw(
            self,
            src_ip: str,
            grouping: Optional[str] = "siteName",
            snapshot_id: Optional[str] = None
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
                groupBy=grouping
            ),
            snapshot=snapshot_id or self.client.snapshot_id
        )
        return self._query(payload)

    @staticmethod
    def check_proto(parameters, flags) -> dict:
        """
        Checks parameters and flags
        :param parameters: dict: Data to Post
        :param flags: list: List of optional TCP flags
        :return: dict: formatted parameters, removing ports if icmp
        """
        if parameters['protocol'] == 'tcp' and flags:
            if all(x in ['ack', 'fin', 'psh', 'rst', 'syn', 'urg'] for x in flags):
                parameters['flags'] = flags
            else:
                raise SyntaxError("Only accepted TCP flags are ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']")
        elif parameters['protocol'] == 'icmp':
            parameters.pop('startingPort', None)
            parameters.pop('destinationPort', None)
            parameters.pop('sourcePort', None)
            parameters.pop('groupPort', None)
        return parameters

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
